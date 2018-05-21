# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.utils.timezone import utc
from django.conf import settings

from datetime import datetime
from django.utils.timezone import utc

from zonetable.apps.accounts.models import UserProfile
from zonetable.apps.home.models import State, Country
from zonetable.apps.directory.models import Directory, Reserve
from zonetable.apps.functions.forms import WhoisForm
from zonetable.apps.functions.views import PointByScore, getUserCountry
from zonetable.apps.directory.forms import ReserveForm

# vista para listar Reservaciones
@login_required(login_url='/')
def list_reservation_view(request, id_sheets, id_page):
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

    pais_actual = Country.objects.all().get(id_country=country_id)

    points = 0
    message = ''
    profile_sent = False

    if request.user.is_authenticated():

        #user = User.objects.get(pk=request.user.id)
        try:
            directory = Directory.objects.get(pk=id_sheets, user=request.user.id)

            reservations = Reserve.objects.filter(directory=directory).order_by('status', 'date', 'time')

            points = PointByScore(request)

            # paginar los resultados a '10' por pagina
            paginator = Paginator(reservations, 10)
            try:
                num_page = int(id_page)
            except:
                num_page = 1
            try:
                reservations = paginator.page(num_page)
            except (EmptyPage, InvalidPage):
                reservations = paginator.page(paginator.num_pages)

        except Directory.DoesNotExist:
            return HttpResponseRedirect('/accounts/sheets/1/')

    else:
        return HttpResponseRedirect('/')

    # enviamos el ID del pais de la cookie
    formulario_whois = WhoisForm(initial={'Country': country_id})

    ctx = {
        'points': points,
        'directory': directory,
        'list_reservations': reservations,
        'formulario_whois': formulario_whois,
        'pais_actual': pais_actual,
    }

    response = render_to_response('accounts/reservation/list.html', ctx, context_instance=RequestContext(request))
    return response

# vista para Crear una Reservacion
@login_required(login_url='/')
def add_reservation_view(request, id_sheets):
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

    pais_actual = Country.objects.all().get(id_country=country_id)

    points = 0
    message = ''
    form_sent = False

    if request.user.is_authenticated():

        #user = User.objects.get(pk=request.user.id)
        try:
            directory = Directory.objects.get(pk=id_sheets, status=True, user=request.user.id)

            points = PointByScore(request)

            if request.method == "POST":
                form_reserve = ReserveForm(request.POST)

                if form_reserve.is_valid():
                    id_user = request.POST.get('id_user')
                    nombre = form_reserve.cleaned_data['name']
                    email_to_user = form_reserve.cleaned_data['email']
                    telefono = form_reserve.cleaned_data['phone']
                    fecha = form_reserve.cleaned_data['date']
                    hora = form_reserve.cleaned_data['time']
                    description = form_reserve.cleaned_data['description']

                    add_reserve = form_reserve.save(commit=False)

                    if id_user:
                        add_reserve.user_id = id_user

                    add_reserve.directory = directory
                    add_reserve.date_create = datetime.now().replace(tzinfo=utc)
                    add_reserve.date_update = datetime.now().replace(tzinfo=utc)

                    add_reserve.save()

                    form_sent = True
            else:
                form_reserve = ReserveForm(initial={'type': 0})

        except Directory.DoesNotExist:
            return HttpResponseRedirect('/accounts/my-reservations/1/')

    else:
        return HttpResponseRedirect('/')

    # enviamos el ID del pais de la cookie
    formulario_whois = WhoisForm(initial={'Country': country_id})

    ctx = {
        'points': points,
        'form_sent': form_sent,
        'form_reserve': form_reserve,
        'directory': directory,
        'formulario_whois': formulario_whois,
        'pais_actual': pais_actual,
    }

    response = render_to_response('accounts/reservation/add.html', ctx, context_instance=RequestContext(request))
    return response

# vista para Editar una Reservacion
@login_required(login_url='/')
def edit_reservation_view(request, id_sheets, id_reservation):
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

    pais_actual = Country.objects.all().get(id_country=country_id)

    points = 0
    message = ''
    form_sent = False

    if request.user.is_authenticated():

        try:
            reservation = Reserve.objects.get(pk=id_reservation, directory=id_sheets)

            directory = Directory.objects.get(pk=id_sheets, status=True, user=request.user.id)

            points = PointByScore(request)

            if request.method == "POST":
                form_reserve = ReserveForm(request.POST, instance=reservation)
                form_reserve.fields['email'].widget.attrs['readonly'] = True

                if form_reserve.is_valid():
                    nombre = form_reserve.cleaned_data['name']
                    email_to_user = form_reserve.cleaned_data['email']
                    telefono = form_reserve.cleaned_data['phone']
                    fecha = form_reserve.cleaned_data['date']
                    hora = form_reserve.cleaned_data['time']
                    description = form_reserve.cleaned_data['description']

                    add_reserve = form_reserve.save(commit=False)

                    add_reserve.directory = directory
                    add_reserve.date_create = datetime.now().replace(tzinfo=utc)
                    add_reserve.date_update = datetime.now().replace(tzinfo=utc)

                    add_reserve.save()

                    form_sent = True
            else:
                form_reserve = ReserveForm(instance=reservation)
                form_reserve.fields['email'].widget.attrs['readonly'] = True

        except:
            return HttpResponseRedirect('/accounts/sheets/1/')

    else:
        return HttpResponseRedirect('/')

    # enviamos el ID del pais de la cookie
    formulario_whois = WhoisForm(initial={'Country': country_id})

    ctx = {
        'points': points,
        'form_sent': form_sent,
        'form_reserve': form_reserve,
        'directory': directory,
        'formulario_whois': formulario_whois,
        'pais_actual': pais_actual,
    }

    response = render_to_response('accounts/reservation/edit.html', ctx, context_instance=RequestContext(request))
    return response

# vista para definir el Status de la Reservacion
@login_required(login_url='/')
def set_status_reservation_view(request, id_sheets, id_reservation, url_name):
    if request.user.is_authenticated():
        try:
            directory = Directory.objects.get(pk=id_sheets, status=True, user=request.user.id)
            reservations = Reserve.objects.get(pk=id_reservation, directory=directory)

            if url_name == 'pending':
                status = 0
            elif url_name == 'process':
                status = 1
            elif url_name == 'cancel':
                status = 2
            elif url_name == 'expire':
                status = 3
            elif url_name == 'complete':
                status = 4
                reservations.score = request.POST.get('score')

            reservations.status = status

            reservations.save()

        except:
            msg = 'error'

    return HttpResponseRedirect('/accounts/reservation/' + id_sheets + '/1/')
