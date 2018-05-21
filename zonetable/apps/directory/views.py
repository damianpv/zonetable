# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives # Enviamos HTML
from django.conf import settings
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg

from django.http import HttpResponse
from django.core import serializers
#from django.utils import simplejson
from datetime import datetime
from django.utils.timezone import utc

from zonetable.apps.accounts.models import UserProfile
from zonetable.apps.home.models import State, Country
from zonetable.apps.directory.models import Category, Directory, Stat, Comment, Rate
from zonetable.apps.functions.forms import WhoisForm
from zonetable.apps.directory.forms import SearchRestaurantForm, ReserveForm, CommentForm, RateForm
from zonetable.apps.multiuploader.models import MultiuploaderImage
from zonetable.apps.functions.views import send_mail
from zonetable.apps.functions.views import PointByScore, getUserCountry

# obtener listado de restaurantes
def get_rest_view(request):
    #se obtienen todos los estados del pais
    state = Directory.objects.filter(status=True, deleted=False)
    #se devuelven los estados en formato json, solo nos interesa obtener como json
    #el id y el estado.
    data = serializers.serialize('json', state, fields=('id_directory','title'))
    return HttpResponse(data, mimetype='application/javascript')

    # creando un json de forma simple sin serializar
    '''
    to_json = {
        "key1": "value1",
        "key2": "value2"
    }
    return HttpResponse(simplejson.dumps(to_json), mimetype='application/json')
    '''

def directory_view(request, url_name):
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

    logged = False
    points = 0

    if request.user.is_authenticated():
        user = User.objects.get(pk=request.user.id)
        profile = UserProfile.objects.get(user=user)
        logged = True

        points = PointByScore(request)


    today = datetime.now()
    today = today.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    max_age = 90*24*60*60 # 3 meses (90 días)
    ###############################

    pais_actual = Country.objects.all().get(id_country=country_id)
    category = Category.objects.all().filter(status=True, type=1, directory__isnull=False, directory__country_id=country_id, directory__deleted=False, directory__status=True).order_by('title').distinct()

    try:
        directory_detail	= Directory.objects.get(url_name=url_name, deleted=False)
        directory_service	= directory_detail.service.all()
        directory_payment	= directory_detail.payment.all()
        directory_style		= directory_detail.style.all()
        directory_category	= directory_detail.category.all()
        galery				= MultiuploaderImage.objects.all().filter(directory_id=directory_detail.id_directory)

        try:
            stat = Stat.objects.get(directory_id=directory_detail.id_directory, date=datetime.now().replace(tzinfo=utc))
            stat.count = int(stat.count) + int(1)
        except Stat.DoesNotExist:
            stat = Stat()
            stat.directory_id = directory_detail.id_directory
            stat.date = datetime.now().replace(tzinfo=utc)
            stat.count = 1

        stat.save()

        form_reserve_sent = False
        form_comment_sent = False

        # crear una reservación
        if "reserve" in request.POST:
            form_reserve = ReserveForm(request.POST)
            if form_reserve.is_valid():
                form_reserve_sent = True

                nombre 			= form_reserve.cleaned_data['name']
                email_to_user 	= form_reserve.cleaned_data['email']
                telefono		= form_reserve.cleaned_data['phone']
                fecha 			= form_reserve.cleaned_data['date']
                hora 			= form_reserve.cleaned_data['time']
                description 	= form_reserve.cleaned_data['description']

                add_reserve				= form_reserve.save(commit=False)
                add_reserve.directory 	= directory_detail
                if logged:
                    add_reserve.user 	= user
                add_reserve.date_create = datetime.now().replace(tzinfo=utc)
                add_reserve.date_update = datetime.now().replace(tzinfo=utc)
                add_reserve.save()

                #enviar Email
                email_from = settings.EMAIL_FROM
                email_to = email_to_user
                subject = 'ZoneTable - Reserva en línea'
                page_url = 'reserve_online.html'
                content = '<p>Hola :</p>'
                content += '<p><strong>Le enviamos los detalles de la Reservaci&oacute;n.</strong></p>'
                content += '<p></p>'
                content += '<p>Lugar: <strong>%s</strong> (<a href="%s">Ver Lugar</a>)</p>' % (directory_detail.title, settings.URL_SITE+directory_detail.url_name)
                content += '<p>Nombre: %s</p>' % (nombre)
                content += '<p>Email: %s</p>' % (email_to_user)
                content += '<p>Tel&eacute;fono: %s</p>' % (telefono)
                content += '<p>Fecha: %s</p>' % (fecha)
                content += '<p>Hora: %s</p>' % (hora)
                content += '<p>Descripci&oacute;n: %s</p>' % (description)
                content += '<br />'
                content += '<p>Te esperamos,</p>'

                send_mail(email_from, email_to, subject, content, page_url, headers=None)

                #enviar Email
                email_from = settings.EMAIL_FROM
                email_to = directory_detail.email
                subject = 'ZoneTable - Reserva en línea'
                page_url = 'reserve_online.html'
                content = '<p>Hola :</p>'
                content += '<p>Haz recibido una nueva reservaci&oacute;n.</p>'
                content += '<p>Lugar: <strong>%s</strong> (<a href="%s">Ver Lugar</a>)</p>' % (directory_detail.title, settings.URL_SITE+directory_detail.url_name)
                content += '<p></p>'
                content += '<p><strong>Detalles del comensal:</strong></p>'
                content += '<p>Nombre: %s</p>' % (nombre)
                content += '<p>Email: %s</p>' % (email_to_user)
                content += '<p>Tel&eacute;fono: %s</p>' % (telefono)
                content += '<p>Fecha: %s</p>' % (fecha)
                content += '<p>Hora: %s</p>' % (hora)
                content += '<p>Descripci&oacute;n: %s</p>' % (description)
                content += '<br />'
                content += '<p>No olvides mantener actualizado tu establecimiento.</p>'

                send_mail(email_from, email_to, subject, content, page_url, headers=None)

        else:
            initial = ''
            if logged:
                initial = {
                            'name':user.first_name + ' ' + user.last_name,
                            'email':user.email,
                            'address':profile.address,
                            'phone':profile.phone,
                }
            form_reserve = ReserveForm(initial=initial)

        # crear un comentario

        if 'comment0' in request.POST:
            form_comment = CommentForm(request.POST)
            if form_comment.is_valid():

                form_comment_sent = True

                add_comment				= form_comment.save(commit=False)
                add_comment.directory 	= directory_detail
                if logged:
                    add_comment.user 	= user
                add_comment.status	= False
                add_comment.date_create	= datetime.now().replace(tzinfo=utc)
                add_comment.save()
        else:
            initial = ''
            if logged:
                initial = {
                    'name':user.first_name + ' ' + user.last_name,
                    'email':user.email,
                }
            form_comment = CommentForm(initial=initial)

        # enviamos el ID del pais de la cookie
        formulario_whois = WhoisForm(initial={'Country':country_id})

        list_comment = Comment.objects.all().filter(status=True, directory=directory_detail).order_by('-pk')[:5]
        list_rate 	 = Rate.objects.all().filter(directory=directory_detail)
        avg 	 	 = Rate.objects.all().filter(directory=directory_detail).aggregate(Avg('value'))

        ctx = {
            'points':points,
            'directory_detail':directory_detail,
            'directory_service':directory_service,
            'directory_payment':directory_payment,
            'directory_style':directory_style,
            'logged':logged,
            'galery':galery,
            'form_reserve_sent':form_reserve_sent,
            'form_comment_sent':form_comment_sent,
            'form_reserve':form_reserve,
            'form_comment':form_comment,
            'formulario_whois':formulario_whois,
            'list_category':category,
            'list_comment':list_comment,
            'list_rate':list_rate,
            'avg':avg,
            'pais_actual':pais_actual,
            'URL_SITE':settings.URL_SITE,
        }

        response = render_to_response('directory/dir.html',ctx,context_instance=RequestContext(request))
        return response
    except Directory.DoesNotExist:
        raise Http404
    return HttpResponseRedirect('/')

def directory_test_view(request):
    url_name = 'gallo-71'

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

    ###############################

    pais_actual = Country.objects.all().get(id_country=country_id)
    category = Category.objects.all().filter(status=True, type=1, directory__isnull=False, directory__country_id=country_id, directory__deleted=False, directory__status=True).order_by('title').distinct()

    points = 0

    if request.user.is_authenticated():
        points = PointByScore(request)

    directory_detail	= Directory.objects.get(url_name=url_name, deleted=False)
    directory_service	= directory_detail.service.all()
    directory_payment	= directory_detail.payment.all()
    directory_style		= directory_detail.style.all()
    galery				= MultiuploaderImage.objects.all().filter(directory_id=directory_detail.id_directory)

    form_reserve_sent = False

    ctx = {
        'points':points,
        'directory_detail':directory_detail,
        'directory_service':directory_service,
        'directory_payment':directory_payment,
        'directory_style':directory_style,
        'galery':galery,
        'form_reserve_sent':form_reserve_sent,
        'list_category':category,
        'pais_actual':pais_actual,
    }

    response = render_to_response('directory/dir_test.html',ctx,context_instance=RequestContext(request))
    return response

def category_view(request):
    category = Category.objects.all()

    return render_to_response('directory/dir.html',context_instance=RequestContext(request))

def directory_category_view(request, url_name, page):
    try:
        country_id = request.COOKIES['gm_country']
        state_id = request.COOKIES['gm_state']
        language_id = request.COOKIES['gm_language']
        # directorio
        directory = Directory.objects.filter(status=True, deleted=False, country_id=country_id, category__url_name__exact=url_name).order_by('-id_directory')
    except:
        #remote_addr = request.META.get('HTTP_X_FORWARDED_FOR', "127.0.0.1")
        remote_addr = request.META['REMOTE_ADDR']
        country_id = getUserCountry(remote_addr)

        state_id = 1
        language_id = 1
        # directorio
        directory = Directory.objects.filter(status=True, deleted=False, category__url_name__exact=url_name).order_by('-id_directory')

    points = 0
    if request.user.is_authenticated():
        user = User.objects.get(pk=request.user.id)
        profile = UserProfile.objects.get(user=user)

        points = PointByScore(request)

        state_id = profile.state_id
        country_id = profile.country_id
        language_id = profile.language_id

    today = datetime.now()
    today = today.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    max_age = 90*24*60*60 # 3 meses (90 días)

    ###############################

    get_category = Category.objects.all().get(url_name=url_name)
    pais_actual = Country.objects.all().get(id_country=country_id)

    # paginar los resultados a '10' por pagina
    paginator = Paginator(directory, 10)
    try:
        num_page = int(page)
    except:
        num_page = 1
    try:
        directory = paginator.page(num_page)
    except (EmptyPage,InvalidPage):
        directory = paginator.page(paginator.num_pages)

    if request.POST:
        formulario = SearchRestaurantForm(request.POST)
    else:
        #formulario = SearchRestaurantForm(initial={'Estado':'4'})
        formulario = SearchRestaurantForm()
        formulario.fields['Estado'].queryset = State.objects.filter(country_id=country_id)

    # enviamos el ID del pais de la cookie
    formulario_whois = WhoisForm(initial={'Country':country_id})

    # categorias
    # type: (1: restaurantes, 2: proveedores)
    category = Category.objects.all().filter(status=True, type=1, directory__isnull=False, directory__country_id=country_id, directory__deleted=False, directory__status=True).order_by('title').distinct()
    #category = Directory.objects.values('category').annotate(Count('category')).order_by()
    #category = Category.objects.annotate(num_category=Count('directory'))
    #category = Directory.objects.annotate(review_count=Count('category')).order_by('review_count')

    #directorio1 = Directorio.objects.filter(status=True)
    ctx = {
        'points':points,
        'form_rest':formulario,
        'list_directory':directory,
        'list_category':category,
        'get_category':get_category,
        'formulario_whois':formulario_whois,
        'pais_actual':pais_actual,
        'url_name':url_name,
    }
    response = render_to_response('directory/directory_x_category.html', ctx, context_instance=RequestContext(request))
    return response

@csrf_exempt
def set_rate_view(request):

    '''
    form_rate = RateForm()
    form_rate.directory = 1
    form_rate.value = 1
    form_rate.date_create = datetime.now().replace(tzinfo=utc)
    form_rate.save()
    '''
    id_dir = request.POST.get('id_dir')
    value = request.POST.get('value')
    date_create = datetime.now().replace(tzinfo=utc)
    r = Rate(directory_id=id_dir,value=value, date_create=date_create)
    r.save()

    ctx = {
        'content':value,
        #'content':'Tu voto: ' + value,
    }
    return render_to_response('functions/content.html', ctx, context_instance=RequestContext(request))
