# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.utils.timezone import utc
from django.template.defaultfilters import slugify
from django.db.models import Sum
from django.conf import settings

from datetime import datetime, timedelta
#import logging

from zonetable.apps.home.models import State, Country
from zonetable.apps.accounts.models import UserProfile
from zonetable.apps.functions.forms import WhoisForm
from zonetable.apps.directory.models import Category, Directory, Package, Pay
from zonetable.apps.accounts.sheets.forms import addRestaurantForm, PackageForm
from zonetable.apps.multiuploader.models import MultiuploaderImage
from zonetable.apps.functions.views import PointByScore, getUserCountry


@login_required(login_url='/')
def list_sheets_view(request, page):
    try:
        country_id = request.COOKIES['gm_country']
        state_id = request.COOKIES['gm_state']
        language_id = request.COOKIES['gm_language']
    except:
        #remote_addr = request.META.get('HTTP_X_FORWARDED_FOR', "127.0.0.1")
        remote_addr = request.META['REMOTE_ADDR']
        country_id = getUserCountry(remote_addr)

    state_id = 1
    language_id = 1


    today = datetime.now()
    today = today.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    max_age = 90 * 24 * 60 * 60 # 3 meses (90 días)

    ###############################

    directory = ''
    message = ''

    if request.user.is_authenticated():
        user = User.objects.get(pk=request.user.id)
        profile = UserProfile.objects.get(user=user)

        points = PointByScore(request)

        directory = Directory.objects.filter(user=user, deleted=False).order_by('-id_directory')
        #TODO: Incluir en el listado las categorías de cada ficha

        # paginar los resultados a '10' por pagina
        paginator = Paginator(directory, 10)
        try:
            num_page = int(page)
        except:
            num_page = 1
        try:
            directory = paginator.page(num_page)
        except (EmptyPage, InvalidPage):
            directory = paginator.page(paginator.num_pages)

    pais_actual = Country.objects.all().get(id_country=country_id)

    # enviamos el ID del pais de la cookie
    formulario_whois = WhoisForm(initial={'Country': country_id})

    ctx = {
        'points': points,
        'num_page': num_page,
        'list_directory': directory,
        'formulario_whois': formulario_whois,
        'pais_actual': pais_actual,
        'message': message,
    }

    response = render_to_response('accounts/sheets/list.html', ctx, context_instance=RequestContext(request))
    return response


@login_required(login_url='/')
def add_sheets_view(request):
    try:
        country_id = request.COOKIES['gm_country']
        state_id = request.COOKIES['gm_state']
        language_id = request.COOKIES['gm_language']
    except:
        #remote_addr = request.META.get('HTTP_X_FORWARDED_FOR', "127.0.0.1")
        remote_addr = request.META['REMOTE_ADDR']
        country_id = getUserCountry(remote_addr)

    state_id = 1
    language_id = 1


    today = datetime.now()
    today = today.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    max_age = 90 * 24 * 60 * 60 # 3 meses (90 días)

    ###############################

    directory = message = msg_error = ''
    pay_count = 0
    form_sent = False
    today = datetime.now()
    formulario = ''
    if request.user.is_authenticated():
        user = User.objects.get(pk=request.user.id)
        profile = UserProfile.objects.get(user=user)

        points = PointByScore(request)

        #try:
        #	pay_count = Pay.objects.filter(user=user, pay_status=3, directory__isnull=True).latest('pk')


        if request.method == "POST":
            formulario = addRestaurantForm(request.POST, request.FILES)
            if formulario.is_valid():
                form_sent = True
                # Agregar restaurante
                add_directory = formulario.save(commit=False)
                add_directory.user = user
                add_directory.url_name = slugify(formulario.cleaned_data['title'])
                add_directory.date_create = datetime.now().replace(tzinfo=utc)
                add_directory.date_update = datetime.now().replace(tzinfo=utc)
                add_directory.save()
                formulario.save_m2m()

                #pay_count.directory = add_directory
                #pay_count.save()

                message = 'Su establecimiento se ha creado satisfactoriamente.'
        else:
            formulario = addRestaurantForm(initial={'country': country_id, 'state': state_id})

        #except Pay.DoesNotExist:
        #	return HttpResponseRedirect('/accounts/sheets/package/')

    pais_actual = Country.objects.all().get(id_country=country_id)

    # enviamos el ID del pais de la cookie
    formulario_whois = WhoisForm(initial={'Country': country_id})

    ctx = {
        'points': points,
        'form_sent': form_sent,
        'state': state_id,
        'list_directory': directory,
        'formulario_whois': formulario_whois,
        'form': formulario,
        'pais_actual': pais_actual,
        'message': message,
        'msg_error': msg_error,
    }

    response = render_to_response('accounts/sheets/add.html', ctx, context_instance=RequestContext(request))
    return response


@login_required(login_url='/')
def edit_sheets_view(request, id_directory):
    try:
        country_id = request.COOKIES['gm_country']
        state_id = request.COOKIES['gm_state']
        language_id = request.COOKIES['gm_language']
    except:
        #remote_addr = request.META.get('HTTP_X_FORWARDED_FOR', "127.0.0.1")
        remote_addr = request.META['REMOTE_ADDR']
        country_id = getUserCountry(remote_addr)

    state_id = 1
    language_id = 1


    today = datetime.now()
    today = today.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    max_age = 90 * 24 * 60 * 60 # 3 meses (90 días)

    ###############################

    directory = ''
    message = ''
    msg_error = ''
    form_sent = False
    today = datetime.now()
    formulario = ''

    if request.user.is_authenticated():
        user = User.objects.get(pk=request.user.id)
        profile = UserProfile.objects.get(user=user)

        points = PointByScore(request)

        try:
            directory = Directory.objects.get(pk=id_directory, user=user)

            '''
                if request.method == "GET":

                    # filtramos las categorias que son seleccionadas
                    category_ids = []
                    for group in d.category.all():
                        category_ids.append(group.pk)

                    formulario = CreateRestaurantForm(initial={
                        'titulo': d.title,
                        'direccion': d.address,
                        'codigo_postal': d.postal_code,
                        'ciudad': d.city,
                        'estado': d.state,
                        'pais': d.country,
                        'categoria':category_ids,
                        'telefono': d.phone,
                        'celular': d.cell,
                        'email': d.email,
                        'sitio_web': d.website,
                        'twitter': d.twitter,
                        'facebook': d.facebook,
                        'google_plus': d.google_plus,
                        'contenido': d.content,
                        'comentarios': int(d.comment),
                        'ubicacion_gmap': d.geo_location,
                        })
                '''
            if request.method == "POST":
                formulario = addRestaurantForm(request.POST, request.FILES, instance=directory)
                if formulario.is_valid():
                    # Agregar restaurante

                    edit_directory = formulario.save(commit=False)
                    formulario.save_m2m()
                    edit_directory.date_update = datetime.now().replace(tzinfo=utc)
                    edit_directory.save() # Guardamos el objeto

                    '''
                        directory.title = formulario.cleaned_data['titulo']
                        directory.address = formulario.cleaned_data['direccion']

                        if formulario.cleaned_data['codigo_postal']:
                            directory.postal_code = formulario.cleaned_data['codigo_postal']
                        if formulario.cleaned_data['ciudad']:
                            directory.city = formulario.cleaned_data['ciudad']

                        directory.state = formulario.cleaned_data['estado']
                        directory.delete =  False
                        directory.country = formulario.cleaned_data['pais']

                        directory.language_id = request.COOKIES['gm_language']
                        #directory.hours = formulario.cleaned_data['horario']
                        directory.phone = formulario.cleaned_data['telefono']

                        if formulario.cleaned_data['celular']:
                            directory.cell = formulario.cleaned_data['celular']

                        directory.email = formulario.cleaned_data['email']

                        if formulario.cleaned_data['sitio_web']:
                            directory.website = formulario.cleaned_data['sitio_web']

                        directory.comment = int(formulario.cleaned_data['comentarios'])

                        if formulario.cleaned_data['contenido']:
                            directory.content = formulario.cleaned_data['contenido']
                        if formulario.cleaned_data['ubicacion_gmap']:
                            directory.geo_location = formulario.cleaned_data['ubicacion_gmap']
                        if formulario.cleaned_data['twitter']:
                            directory.twitter = formulario.cleaned_data['twitter']
                        if formulario.cleaned_data['facebook']:
                            directory.facebook = formulario.cleaned_data['facebook']
                        if formulario.cleaned_data['google_plus']:
                            directory.google_plus = formulario.cleaned_data['google_plus']

                        directory.url_name = slugify(formulario.cleaned_data['titulo'])
                        directory.user = user
                        directory.date_create = datetime.now().replace(tzinfo=utc)

                        try:
                            directory.save()
                            directory.category.clear()
                            category = request.POST.getlist('categoria')
                            for i in category:
                                directory.category.add(i)
                            form_sent = True
                        except:
                            msg_error = 'Error: Se produjo un error al guardar los datos.'
                        '''
                    form_sent = True
                    message = 'Su ficha se ha editado satisfactoriamente.'
            else:
                formulario = addRestaurantForm(instance=directory)
        except:
            return HttpResponseRedirect('/accounts/sheets/1/')

    pais_actual = Country.objects.all().get(id_country=country_id)

    # enviamos el ID del pais de la cookie
    formulario_whois = WhoisForm(initial={'Country': country_id})

    ctx = {
        'points': points,
        'form_sent': form_sent,
        'state': state_id,
        'list_directory': directory,
        'formulario_whois': formulario_whois,
        'form': formulario,
        'pais_actual': pais_actual,
        'message': message,
        'msg_error': msg_error,
    }

    response = render_to_response('accounts/sheets/edit.html', ctx, context_instance=RequestContext(request))
    return response


@login_required(login_url='/')
def delete_sheets_view(request, id_directory):
    directory = Directory.objects.get(pk=id_directory)
    directory.status = False
    directory.deleted = True
    directory.save()

    return HttpResponseRedirect('/accounts/sheets/1/')


@login_required(login_url='/')
def activate_sheets_view(request, id_directory):
    directory = Directory.objects.get(pk=id_directory)
    directory.status = True
    directory.save()

    return HttpResponseRedirect('/accounts/sheets/1/')


@login_required(login_url='/')
def deactivate_sheets_view(request, id_directory):
    directory = Directory.objects.get(pk=id_directory)
    directory.status = False
    directory.save()

    return HttpResponseRedirect('/accounts/sheets/1/')


@login_required(login_url='/')
def gallery_sheets_view(request, id_directory):
    try:
        country_id = request.COOKIES['gm_country']
        state_id = request.COOKIES['gm_state']
        language_id = request.COOKIES['gm_language']
    except:
        #remote_addr = request.META.get('HTTP_X_FORWARDED_FOR', "127.0.0.1")
        remote_addr = request.META['REMOTE_ADDR']
        country_id = getUserCountry(remote_addr)

    state_id = 1
    language_id = 1


    today = datetime.now()
    today = today.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    max_age = 90 * 24 * 60 * 60 # 3 meses (90 días)

    ###############################

    directory = ''
    message = ''
    msg_error = ''
    form_sent = False
    today = datetime.now()

    if request.user.is_authenticated():
        user = User.objects.get(pk=request.user.id)
        profile = UserProfile.objects.get(user=user)

        d = Directory.objects.get(pk=id_directory)

        points = PointByScore(request)

    pais_actual = Country.objects.all().get(id_country=country_id)

    # enviamos el ID del pais de la cookie
    formulario_whois = WhoisForm(initial={'Country': country_id})

    items = MultiuploaderImage.objects.all()

    #logger = logging.getLogger('my_app_name.my_new_module')
    #logger.debug('Hello logs!')

    ctx = {
        'points': points,
        'id_directory': id_directory,
        'items': items,
        'form_sent': form_sent,
        'state': state_id,
        'formulario_whois': formulario_whois,
        'pais_actual': pais_actual,
        'message': message,
        'msg_error': msg_error,
    }

    return render_to_response('accounts/sheets/gallery.html', ctx, context_instance=RequestContext(request))


def list_package_view(request):
    try:
        country_id = request.COOKIES['gm_country']
        state_id = request.COOKIES['gm_state']
        language_id = request.COOKIES['gm_language']
    except:
        #remote_addr = request.META.get('HTTP_X_FORWARDED_FOR', "127.0.0.1")
        remote_addr = request.META['REMOTE_ADDR']
        country_id = getUserCountry(remote_addr)

    state_id = 1
    language_id = 1


    today = datetime.now()
    today = today.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    max_age = 90 * 24 * 60 * 60 # 3 meses (90 días)

    ###############################

    message = ''
    msg_error = ''
    form_sent = ''
    last_id = 0
    pay_months = 0
    total_price = 0
    concept = ''

    pais_actual = Country.objects.all().get(id_country=country_id)

    list_package = Package.objects.filter(status=True).order_by('order')
    total_package = Package.objects.all().aggregate(price=Sum('price'))

    if request.user.is_authenticated():
        user = User.objects.get(pk=request.user.id)

        points = PointByScore(request)

    if request.method == "POST":
        form_package = PackageForm(request.POST)
        if form_package.is_valid():
            fecha = datetime.now().replace(tzinfo=utc)

            form_sent = True
            package = form_package.save(commit=False)
            package.user = user
            package.pay_status = 1
            package.subtotal = request.POST['subtotal']
            package.date_create = fecha
            package.date_begin = fecha
            package.date_end = fecha
            package.save() # Guardamos el objeto
            form_package.save_m2m()
            last_id = package.pk
            pay_months = package.pay_months
            total_price = package.price
            concept = package.concept
    else:
        form_sent = False
        form_package = PackageForm()

    # enviamos el ID del pais de la cookie
    formulario_whois = WhoisForm(initial={'Country': country_id})

    paypal_email = settings.PAYPAL_EMAIL
    paypal_url = settings.PAYPAL_URL
    paypal_return_url = settings.PAYPAL_RETURN_URL
    paypal_cancel_url = settings.PAYPAL_RETURN_URL + '%s/cancel/' % (last_id)

    ctx = {
        'points': points,
        'pay_id': last_id,
        'paypal_email': paypal_email,
        'paypal_url': paypal_url,
        'paypal_return_url': paypal_return_url,
        'paypal_cancel_url': paypal_cancel_url,
        'total_price': total_price,
        'concept': concept,
        'pay_months': pay_months,
        'total_package': total_package,
        'list_package': list_package,
        'form_package': form_package,
        'formulario_whois': formulario_whois,
        'pais_actual': pais_actual,
        'form_sent': form_sent,
        'message': message,
    }

    response = render_to_response('accounts/sheets/package.html', ctx, context_instance=RequestContext(request))
    return response
