# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
#from django.core.mail import EmailMultiAlternatives # Enviamos HTML
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.db.models import Count
from django.utils.timezone import utc
from datetime import datetime

from zonetable.apps.home.models import Contact, Content, State, Country
from zonetable.apps.home.forms import ContactForm
from zonetable.apps.functions.forms import WhoisForm
from zonetable.apps.directory.forms import SearchRestaurantForm
from zonetable.apps.accounts.forms import LoginForm
from zonetable.apps.directory.models import Category, Directory, Package
from zonetable.apps.functions.views import send_mail, PointByScore, getUserCountry
from zonetable.apps.accounts.models import UserProfile
from zonetable.apps.multiuploader.models import MultiuploaderImage


def contact_view(request):
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

    contact_sent = False  # Definir si se envio la informacion correctamente o no
    nombre = ''
    email = ''
    telefono = ''
    como_conocio = ''
    asunto = ''
    comentarios = ''
    points = 0

    if request.user.is_authenticated():
        user = User.objects.get(pk=request.user.id)
        profile = UserProfile.objects.get(user=user)

        points = PointByScore(request)

        nombre = user.first_name + ' ' + user.last_name
        email = user.email
        telefono = profile.phone

    today = datetime.now()
    today = today.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    max_age = 90 * 24 * 60 * 60 # 3 meses (90 días)

    ###############################

    pais_actual = Country.objects.all().get(id_country=country_id)

    if request.method == "POST":
        formulario = ContactForm(request.POST)
        if formulario.is_valid():
            contact_sent = True
            email = formulario.cleaned_data['Email']
            nombre = formulario.cleaned_data['Nombre']
            telefono = formulario.cleaned_data['Telefono']
            como_conocio = formulario.cleaned_data['Como_conocio']
            asunto = formulario.cleaned_data['Asunto']
            comentarios = formulario.cleaned_data['Comentarios']

            # Almacenar la info en la BD
            c = Contact()
            c.status = 1
            c.name = nombre
            c.email = email
            c.phone = telefono
            c.language_id = language_id
            c.country_id = country_id
            c.how_know = como_conocio
            c.subject = asunto
            c.content = comentarios
            c.date_create = datetime.now().replace(tzinfo=utc)
            c.save()

            #enviar Email
            email_from = settings.EMAIL_FROM
            email_to = settings.EMAIL_TO
            subject = 'ZoneTable - Contacto'
            page_url = 'contact_admin.html'
            content = '<p>Hola :</p>'
            content += '<p>Ha recibido un nuevo mensaje de contacto.</p>'
            content += '<p>Nombre: %s</p>' % (nombre)
            content += '<p>Email: %s</p>' % (email)
            content += '<p>Tel&eacute;fono: %s</p>' % (telefono)
            content += '<p>Comentarios: %s</p>' % (comentarios)

            send_mail(email_from, email_to, subject, content, page_url, headers=None)

            email_from = settings.EMAIL_FROM
            email_to = email
            subject = 'ZoneTable - Contacto'
            page_url = 'contact_admin.html'
            content = '<p>Hola %s:</p>' % (nombre)
            content += '<p>Le enviamos una copia de su mensaje de contacto a trav&eacute;s del formulario:</p>'
            content += '<p>Nombre: %s</p>' % (nombre)
            content += '<p>Email: %s</p>' % (email)
            content += '<p>Tel&eacute;fono: %s</p>' % (telefono)
            content += '<p>Comentarios: %s</p>' % (comentarios)

            send_mail(email_from, email_to, subject, content, page_url, headers=None)
            #####

            message = 'Su mensaje ha sido enviado satisfactoriamente.'
    else:
        formulario = ContactForm(initial={
            'Nombre': nombre,
            'Email': email,
            'Telefono': telefono
        })

    # enviamos el ID del pais de la cookie
    formulario_whois = WhoisForm(initial={'Country': country_id})

    ctx = {
        'points': points,
        'form': formulario,
        'contact_sent': contact_sent,
        'formulario_whois': formulario_whois,
        'pais_actual': pais_actual,
    }
    response = render_to_response('home/contacto.html', ctx, context_instance=RequestContext(request))
    return response


def content_view(request, url_name):
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
    max_age = 90 * 24 * 60 * 60 # 3 meses (90 días)

    ###############################

    pais_actual = Country.objects.all().get(id_country=country_id)

    content = Content.objects.get(url_name=url_name)

    # enviamos el ID del pais de la cookie
    formulario_whois = WhoisForm(initial={'Country': country_id})

    ctx = {
        'points': points,
        'content': content,
        'formulario_whois': formulario_whois,
        'pais_actual': pais_actual,
    }
    response = render_to_response('home/contenidos.html', ctx, context_instance=RequestContext(request))
    return response


def affiliate_view(request):
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
    max_age = 90 * 24 * 60 * 60 # 3 meses (90 días)

    ###############################

    pais_actual = Country.objects.all().get(id_country=country_id)

    content = Content.objects.get(url_name='affiliate')

    # enviamos el ID del pais de la cookie
    formulario_whois = WhoisForm(initial={'Country': country_id})

    list_package = Package.objects.filter(status=True).order_by('order')

    ctx = {
        'points': points,
        'list_package': list_package,
        'content': content,
        'formulario_whois': formulario_whois,
        'pais_actual': pais_actual,
    }
    response = render_to_response('home/affiliate.html', ctx, context_instance=RequestContext(request))
    return response


def home_view(request):
    #TODO: testing
    try:
        country_id = request.COOKIES['gm_country']
        state_id = request.COOKIES['gm_state']
        language_id = request.COOKIES['gm_language']
        # directorio
        directory = Directory.objects.all().filter(status=True, deleted=False, language_id=language_id,
                                                   country_id=country_id).order_by('-id_directory')[:10]
    except:
        #remote_addr = request.META.get('HTTP_X_FORWARDED_FOR', "127.0.0.1")
        remote_addr = request.META['REMOTE_ADDR']
        country_id = getUserCountry(remote_addr)

        state_id = 1
        language_id = 1
        # directorio
        directory = Directory.objects.all().filter(status=True, deleted=False, language_id=language_id).order_by(
            '-id_directory')[:10]

    points = 0

    if request.user.is_authenticated():
        user = User.objects.get(pk=request.user.id)
        profile = UserProfile.objects.get(user=user)

        points = PointByScore(request)

    today = datetime.now()
    today = today.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    max_age = 90 * 24 * 60 * 60 # 3 meses (90 días)

    ###############################

    pais_actual = Country.objects.all().get(id_country=country_id)
    estado_actual = State.objects.all().get(id_state=state_id)

    '''
	login_sent = False  # Definir si se envio la informacion correctamente o no
	email = ''
	password = ''

	if request.method == "POST":
		formulario = LoginForm(request.POST)
		if formulario.is_valid():
			login_sent = True
			email = formulario.cleaned_data['Email']
	else:
		formulario = LoginForm()
		'''
    if request.POST:
        formulario = SearchRestaurantForm(request.POST)
    else:
        #formulario = SearchRestaurantForm(initial={'Estado':'4'})
        formulario = SearchRestaurantForm(initial={'Estado': state_id})
        formulario.fields['Estado'].queryset = State.objects.filter(country_id=country_id)

    # enviamos el ID del pais de la cookie
    formulario_whois = WhoisForm(initial={'Country': country_id})

    # categorias
    # type: (1: restaurantes, 2: proveedores)
    category = Category.objects.all().filter(status=True, type=1, directory__isnull=False,
                                             directory__country_id=country_id, directory__deleted=False,
                                             directory__status=True).order_by('title').distinct()
    #category = Directory.objects.values('category').annotate(Count('category')).order_by()
    #category = Category.objects.annotate(num_category=Count('directory'))
    #category = Directory.objects.annotate(review_count=Count('category')).order_by('review_count')

    #directorio1 = Directorio.objects.filter(status=True)

    #d = Directory.objects.filter(multiuploaderimage__filename='thumbnail-big.jpg')
    #m = MultiuploaderImage.objects.select_related('directory')

    #lista = d.multiuploaderimage.all()

    #lista = Directory.multiuploaderimage_set.all()[:0]

    ctx = {
        'points': points,
        #'list':lista,
        'form_rest': formulario,
        'list_directory': directory,
        'list_category': category,
        'formulario_whois': formulario_whois,
        'pais_actual': pais_actual,
        'pais_actual1': 'img/flag/%s.gif' % pais_actual.iso2.lower(),
    }
    response = render_to_response('home/index.html', ctx, context_instance=RequestContext(request))
    return response


'''
def home_original_view(request):
	directorio = Directorio.objects.all().filter(status=True).order_by('-id_directorio')[:10]
	#directorio1 = Directorio.objects.filter(status=True)
	ctx = {'listar_directorio':directorio}
	return render_to_response('home/index_orig.html', ctx, context_instance=RequestContext(request))

def home_fb_view(request):
	directorio = Directorio.objects.all().filter(status=True).order_by('-id_directorio')[:10]
	#directorio1 = Directorio.objects.filter(status=True)
	ctx = {'listar_directorio':directorio}
	return render_to_response('home/index_fb.html', ctx, context_instance=RequestContext(request))
'''


def faq_view(request):
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
    max_age = 90 * 24 * 60 * 60 # 3 meses (90 días)

    ###############################

    pais_actual = Country.objects.all().get(id_country=country_id)

    formulario_whois = WhoisForm(initial={'Country': country_id})

    ctx = {
        'points': points,
        'formulario_whois': formulario_whois,
        'pais_actual': pais_actual,
    }
    response = render_to_response('home/faq.html', ctx, context_instance=RequestContext(request))
    return response


'''
def privacy_view(request):
	return render_to_response('home/privacidad.html', context_instance=RequestContext(request))

def terms_view(request):
	return render_to_response('home/terminos.html', context_instance=RequestContext(request))
'''


def test_ip(request):
    return HttpResponse('')

