# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.sessions.backends.db import SessionStore
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from django.template import RequestContext, loader

from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
#from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers
from datetime import datetime
from django.utils.timezone import utc

import random

from zonetable.apps.accounts.forms import LoginForm, ForgotPassForm, UserForm, RegisterForm, EditRegisterForm, ProfileForm
from zonetable.apps.home.models import State, Country
from zonetable.apps.accounts.models import UserProfile
from zonetable.apps.directory.models import Category, Directory, Reserve
from zonetable.apps.directory.forms import ReserveForm
from zonetable.apps.functions.forms import WhoisForm
from zonetable.apps.functions.views import send_mail, PointByScore, getUserCountry

# Funcion para validar si el usuario existe
def user_validate_view(request):
    try:
        value = request.POST.get('value')

        user = User.objects.get(email=value)
        ctx = "%s|%s|%s|%s" % (user.pk, user.email, user.first_name, user.last_name)
    except:
        ctx = 0

    return HttpResponse(ctx)

# obtener listado de estados segun el país por ajax
def get_state_view(request):
    try:
        if request.POST:
            country_id = request.POST.get('country_id')

            #se obtiene el pais
            country = Country.objects.get(id_country=int(country_id))

            #se obtienen todos los estados del pais
            state = State.objects.filter(country_id=country)

            #se devuelven los estados en formato json, solo nos interesa obtener como json
            #el id y el estado.
            data = serializers.serialize('json', state, fields=('id_state', 'state'))
        return HttpResponse(data, mimetype='application/javascript')
    except:
        raise Http404

# confirmar cuenta de usuario
# TODO: actualmente confirma la cuenta en el campo user_status (las cuentas se mantienen activas)
def confirm_view(request, random):
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

    if request.user.is_authenticated():
        user = User.objects.get(pk=request.user.id)
        profile = UserProfile.objects.get(user=user)

        state_id = profile.state_id
        country_id = profile.country_id
        language_id = profile.language_id

    today = datetime.now()
    today = today.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    max_age = 90 * 24 * 60 * 60 # 3 meses (90 días)

    ###############################

    pais_actual = Country.objects.all().get(id_country=country_id)

    message_ok = ''
    message_error = ''

    points = 0

    if request.user.is_authenticated():
        points = PointByScore(request)

    try:
        user_profile = UserProfile.objects.get(random=random)
        #user = User.objects.get(pk=user_profile.user_id)
        #user.is_active = True
        #user.save()
        user_profile.user_status = '1'
        user_profile.save()
        message_ok = 'Felicidades, haz confirmado satisfactoriamente tu cuenta.'

    except UserProfile.DoesNotExist:
        message_error = 'Error: El código de confirmación es incorrecto. <br /> <br /> Por favor, <a href="/contact/">contáctanos aquí</a>.'

    # enviamos el ID del pais de la cookie
    formulario_whois = WhoisForm(initial={'Country': country_id})

    ctx = {
        'points': points,
        'message_ok': message_ok,
        'message_error': message_error,
        'formulario_whois': formulario_whois,
        'pais_actual': pais_actual,
    }
    response = render_to_response('accounts/register_confirm.html', ctx, context_instance=RequestContext(request))
    return response

# login de usuarios vía ajax
def login_view(request):
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
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        if request.POST:
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                #if request.is_ajax:
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        userDates = User.objects.get(email=username)
                        userProfile = UserProfile.objects.get(user_id=userDates.pk)

                        state_id = userProfile.state_id
                        country_id = userProfile.country_id
                        language_id = userProfile.language_id

                        message = 'ok|Login success'
                    else:
                        message = 'error|Error: Su cuenta no está activa. Verifique su email o contáctenos.'
                else:
                    message = 'error|Error: Email y/o contraseña incorrectos.'
            else:
                message = 'error|Error: Por favor, inserte su email y/o contraseña.'
        else:
            form = LoginForm()

        ctx = {
            'form': form,
            'message': message,
        }
        response = render_to_response('accounts/login.html', ctx, context_instance=RequestContext(request))
        response.set_cookie("gm_state", state_id)
        response.set_cookie("gm_country", country_id)
        response.set_cookie("gm_language", language_id)
        return response


# recuperar contraseña vía ajax
def forgot_view(request):
    message = ''
    #if request.user.is_authenticated():
        #return HttpResponseRedirect('/')
    #else:
    if request.POST:
        form = ForgotPassForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['forgot_email']

            try:
                user = User.objects.get(email=email)

                random_number = User.objects.make_random_password(length=10)

                # generate and save the new password
                user.set_password(random_number)
                user.save()

                #enviar Email
                email_from = settings.EMAIL_FROM
                email_to = email
                subject = 'ZoneTable - Recuperar contraseña'
                page_url = 'recovery_pass.html'
                content = '<p>Hola %s:</p>' % (user.first_name)
                content += '<p>Te enviamos tu nueva contrase&ntilde;a: %s</p>' % (random_number)
                content += '<p>Te recomendamos cambiar la contrase&ntilde;a que te hemos enviado. Accede a ZoneTable con ' \
                           'tu cuenta de correo electr&oacute;nico y la contrase&ntilde;a, luego ve a Editar Perfil.</p>'

                send_mail(email_from, email_to, subject, content, page_url, headers=None)
                #####

                """
				password = form.cleaned_data['password']
				user = authenticate(username=username,password=password)
				#if request.is_ajax:
				if user is not None and user.is_active:
					login(request,user)
					message = 'ok'
				else:
					message = 'usuario y/o password incorrecto'
				"""
                message = 'ok|Hemos enviado a tu email una nueva contraseña.'

            except User.DoesNotExist:
                message = 'error|Error: Tu email no está registrado en nuestro sitio.'
        else:
            message = 'error|Error: Inserte su email válido.'
    else:
        form = ForgotPassForm()

    ctx = {
        'form': form,
        'message': message,
    }
    return render_to_response('accounts/forgot_pass.html', ctx, context_instance=RequestContext(request))


# cerrar session del usuario
def logout_view(request):
    logout(request)
    #return HttpResponseRedirect('/?%s' % random.randint(10, 9999))
    return HttpResponseRedirect('/')


# registrar usuario.
def register_view(request):
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

    if request.user.is_authenticated():
        user = User.objects.get(pk=request.user.id)
        profile = UserProfile.objects.get(user=user)

        state_id = profile.state_id
        country_id = profile.country_id
        language_id = profile.language_id

    today = datetime.now()
    today = today.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    max_age = 90 * 24 * 60 * 60 # 3 meses (90 días)

    ###############################

    pais_actual = Country.objects.all().get(id_country=country_id)

    # Envia por email un codigo para confirmar la cuenta de email (la cuenta no se deshabilita, solo se guarda el valor en otro campo).

    register_sent = False  # Definir si se envio la informacion correctamente o no
    message = ''
    first_name = ''
    last_name = ''
    phone = ''
    birth_day = ''
    birth_month = ''
    birth_year = ''
    state = ''
    country = ''
    email = ''
    password = ''
    repassword = ''

    if not request.user.is_authenticated():
        if request.POST:
            form_user = UserForm(request.POST)
            form_profile = RegisterForm(request.POST)

            if form_user.is_valid():
                if form_profile.is_valid():
                    email = form_user.cleaned_data['email']
                    password = form_user.cleaned_data['password']
                    repassword = form_user.cleaned_data['repassword']

                    """
					nombre = form_user.cleaned_data['first_name']
					apellidos = form_user.cleaned_data['last_name']
					telefono = form_profile.cleaned_data['phone']
					nac_dia = form_profile.cleaned_data['nac_dia']
					nac_mes = form_profile.cleaned_data['nac_mes']
					nac_anio = form_profile.cleaned_data['nac_anio']
					estado = form_profile.cleaned_data['estado']
					pais = form_profile.cleaned_data['pais']
					language = language_id
					"""

                    try:
                        User.objects.get(email=email)
                        message = 'Error: El Email ya se encuentra registrado.'
                    #<a href="/forgot_pass/">¿Olvidó su contraseña?</a>

                    except User.DoesNotExist:
                        if password == repassword:
                            register_sent = True
                            # Registro de usuario
                            """
							crear_usuario = User.objects.create_user(username='user_email', email='a')
							crear_usuario.is_active = True
							crear_usuario.save()
							"""

                            random_number = User.objects.make_random_password(length=10)

                            addUser = form_user.save(commit=False)
                            addUser.username = email
                            addUser.set_password(password)
                            addUser.is_active = True
                            addUser.last_login = datetime.now().replace(tzinfo=utc)
                            addUser.date_joined = datetime.now().replace(tzinfo=utc)
                            addUser.save()

                            addProfile = form_profile.save(commit=False)
                            addProfile.user = addUser
                            addProfile.random = random_number
                            addProfile.user_status = False
                            addProfile.save()
                            form_profile.save_m2m()

                            """
							crear_profile = form_profile.save(commit=False)
							crear_profile.user = crear_usuario
							crear_profile.phone = phone
							crear_profile.birth_day = birth_day
							crear_profile.birth_month = birth_month
							crear_profile.birth_year = birth_year
							crear_profile.state = state
							crear_profile.country = country
							crear_profile.language_id = language_id
							crear_profile.random = random_number
							crear_profile.user_status = 0
							crear_profile.save()
							form_profile.save_m2m()
							"""

                            url_confirm = settings.URL_SITE

                            message = 'Su cuenta ha sido creada satisfactoriamente.'
                        else:
                            message = 'Las contraseñas no coinciden.'

                        """
						nombre = formulario.cleaned_data['nombre']
						apellidos = formulario.cleaned_data['apellidos']
						telefono = formulario.cleaned_data['telefono']
						nac_dia = formulario.cleaned_data['nac_dia']
						nac_mes = formulario.cleaned_data['nac_mes']
						nac_anio = formulario.cleaned_data['nac_anio']
						estado = formulario.cleaned_data['estado']
						pais = formulario.cleaned_data['pais']
						language = language_id
						email = formulario.cleaned_data['email']
						password = formulario.cleaned_data['password']
						repassword = formulario.cleaned_data['repassword']

						try:
							User.objects.get(email=email)
							message = 'Error: El Email ya se encuentra registrado.'
							#<a href="/forgot_pass/">¿Olvidó su contraseña?</a>

						except User.DoesNotExist:
							if password == repassword:
								register_sent = True

								crear_usuario = User.objects.create_user(username=email, email=email)
								crear_usuario.first_name = nombre
								crear_usuario.last_name = apellidos
								crear_usuario.set_password(password)
								crear_usuario.is_active = True
								crear_usuario.save()

								random_number = User.objects.make_random_password(length=10)

								perfil_usuario = UserProfile(user=crear_usuario)
								perfil_usuario.phone = telefono
								perfil_usuario.birth_day = nac_dia
								perfil_usuario.birth_month = nac_mes
								perfil_usuario.birth_year = nac_anio
								perfil_usuario.state = estado
								perfil_usuario.country = pais
								perfil_usuario.language_id = language
								perfil_usuario.random = random_number
								perfil_usuario.user_status = 0
								perfil_usuario.save()

								url_confirm = settings.URL_SITE

								#enviar Email
								email_from = settings.EMAIL_FROM
								email_to = email
								subject = 'ZoneTable - Registro'
								page_url = 'register_confirm.html'
								content = '<p>Hola <strong>%s</strong>:</p><p>Muchas gracias por pertenecer a nuestro sitio.</p><p>Por favor, confirma tu email con el siguiente enlace : %sconfirm/%s/</p>' % (nombre, url_confirm, random_number)

								send_mail(email_from, email_to, subject, content, page_url, headers = None)
								#####

								message = 'Su cuenta ha sido creada satisfactoriamente.'
							else:
								message = 'No coinciden.'
						"""
        else:
            # enviamos el ID del pais de la cookie
            form_user = UserForm()
            form_profile = RegisterForm(initial={'country': country_id, 'state': state_id})
        #formulario = RegisterForm()
        #formulario.fields['pais'].queryset = Country.objects.filter(id_country=country_id).order_by('title')

        # enviamos el ID del pais de la cookie
        formulario_whois = WhoisForm(initial={'Country': country_id})

        ctx = {
            'state': state_id,
            'message': message,
            'register_sent': register_sent,
            'form_user': form_user,
            'form_profile': form_profile,
            'formulario_whois': formulario_whois,
            'pais_actual': pais_actual,
        }
        response = render_to_response('accounts/register.html', ctx, context_instance=RequestContext(request))
        return response
    else:
        return HttpResponseRedirect('/')


# registrar usuario referido.
def referer_view(request, id_user):

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

    if request.user.is_authenticated():
        user = User.objects.get(pk=request.user.id)
        profile = UserProfile.objects.get(user=user)

        state_id = profile.state_id
        country_id = profile.country_id
        language_id = profile.language_id

    today = datetime.now()
    today = today.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    max_age = 90 * 24 * 60 * 60 # 3 meses (90 días)

    ###############################

    pais_actual = Country.objects.all().get(id_country=country_id)

    # Envia por email un codigo para confirmar la cuenta de email (la cuenta no se deshabilita, solo se guarda el valor en otro campo).

    register_sent = False  # Definir si se envio la informacion correctamente o no
    message = ''
    first_name = ''
    last_name = ''
    phone = ''
    birth_day = ''
    birth_month = ''
    birth_year = ''
    state = ''
    country = ''
    email = ''
    password = ''
    repassword = ''

    if not request.user.is_authenticated():
        if request.POST:
            form_user = UserForm(request.POST)
            form_profile = RegisterForm(request.POST)

            if form_user.is_valid():
                if form_profile.is_valid():
                    email = form_user.cleaned_data['email']
                    password = form_user.cleaned_data['password']
                    repassword = form_user.cleaned_data['repassword']

                    try:
                        User.objects.get(email=email)
                        message = 'Error: El Email ya se encuentra registrado.'
                    #<a href="/forgot_pass/">¿Olvidó su contraseña?</a>

                    except User.DoesNotExist:
                        if password == repassword:

                            register_sent = True
                            # Registro de usuario
                            random_number = User.objects.make_random_password(length=10)

                            addUser = form_user.save(commit=False)
                            addUser.username = email
                            addUser.set_password(password)
                            addUser.is_active = True
                            addUser.last_login = datetime.now().replace(tzinfo=utc)
                            addUser.date_joined = datetime.now().replace(tzinfo=utc)
                            addUser.save()

                            addProfile = form_profile.save(commit=False)
                            addProfile.user = addUser
                            addProfile.random = random_number
                            addProfile.user_status = False

                            try:
                                referer_user = User.objects.get(pk=id_user)
                                addProfile.referer = referer_user.pk
                            except User.DoesNotExist:
                                pass

                            addProfile.save()
                            form_profile.save_m2m()

                            url_confirm = settings.URL_SITE

                            message = 'Su cuenta ha sido creada satisfactoriamente.'
                        else:
                            message = 'Las contraseñas no coinciden.'

        else:
            # enviamos el ID del pais de la cookie
            form_user = UserForm()
            form_profile = RegisterForm(initial={'country': country_id, 'state': state_id})
        #formulario = RegisterForm()
        #formulario.fields['pais'].queryset = Country.objects.filter(id_country=country_id).order_by('title')

        # enviamos el ID del pais de la cookie
        formulario_whois = WhoisForm(initial={'Country': country_id})

        ctx = {
            'state': state_id,
            'message': message,
            'register_sent': register_sent,
            'form_user': form_user,
            'form_profile': form_profile,
            'formulario_whois': formulario_whois,
            'pais_actual': pais_actual,
        }
        response = render_to_response('accounts/register.html', ctx, context_instance=RequestContext(request))
        return response
    else:
        return HttpResponseRedirect('/')


# login de usuarios de facebook
@csrf_exempt
def user_fb_view(request):
    # los usuarios que accedan mediante facebook se registran como usuario del sitio (no se le envía al usuario una clave de acceso).
    # si acceden y ya están registrados se actualiza la fecha de login para usar como estadística.
    message = ''

    if request.POST:
        try:
            email = request.POST.get('email')
            user = User.objects.get(email=email)

            user.first_name = request.POST.get('fname')
            user.last_name = request.POST.get('lname')
            user.save()

            perfil_usuario = UserProfile.objects.get(user_id=user.pk)
            perfil_usuario.state_id = '1'
            perfil_usuario.country_id = '1'
            perfil_usuario.fb_id = request.POST.get('fbID')
            perfil_usuario.fb_verify = request.POST.get('verified')
            perfil_usuario.gender = request.POST.get('gender')
            perfil_usuario.locale = request.POST.get('locale')
            perfil_usuario.birthday = request.POST.get('birthday')
            perfil_usuario.save()

            from django.contrib.auth import load_backend, login

            if not hasattr(user, 'backend'):
                for backend in settings.AUTHENTICATION_BACKENDS:
                    if user == load_backend(backend).get_user(user.pk):
                        user.backend = backend
                        break

            if hasattr(user, 'backend'):
                login(request, user)

            message = 'Usuario existe.'

        except User.DoesNotExist:
            email = request.POST.get('email')
            crear_usuario = User.objects.create_user(username=email, email=email)
            random_number = User.objects.make_random_password(length=10)

            crear_usuario.first_name = request.POST.get('fname')
            crear_usuario.last_name = request.POST.get('lname')
            crear_usuario.is_active = True
            crear_usuario.save()

            perfil_usuario = UserProfile(user=crear_usuario)
            perfil_usuario.state_id = '1'
            perfil_usuario.random = random_number
            perfil_usuario.user_status = False
            perfil_usuario.country_id = '1'
            perfil_usuario.fb_id = request.POST.get('fbID')
            perfil_usuario.fb_verify = request.POST.get('verified')
            perfil_usuario.gender = request.POST.get('gender')
            perfil_usuario.locale = request.POST.get('locale')
            perfil_usuario.birthday = request.POST.get('birthday')
            perfil_usuario.save()

            from django.contrib.auth import load_backend, login

            if not hasattr(user, 'backend'):
                for backend in settings.AUTHENTICATION_BACKENDS:
                    if user == load_backend(backend).get_user(user.pk):
                        user.backend = backend
                        break

            if hasattr(user, 'backend'):
                login(request, user)

            message = 'Usuario registrado.'
    ctx = {
        'message': message,
    }
    return render_to_response('accounts/user_redsocial.html', ctx, context_instance=RequestContext(request))

# vista para mostrar el dashboard del usuario
@login_required(login_url='/')
def view_dashboard_view(request):
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

    today = datetime.now()
    today = today.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    max_age = 90 * 24 * 60 * 60 # 3 meses (90 días)

    ###############################

    pais_actual = Country.objects.all().get(id_country=country_id)
    category = Category.objects.all().filter(status=True, type=1).order_by('title')

    message = ''
    user = ''
    profile = ''

    if request.user.is_authenticated():
        user = User.objects.get(pk=request.user.id)
        profile = UserProfile.objects.get(user=user)
    else:
        return HttpResponseRedirect('/')

    # enviamos el ID del pais de la cookie
    formulario_whois = WhoisForm(initial={'Country': country_id})

    ctx = {
        'points': points,
        'list_user': user,
        'list_profile': profile,
        'message': message,
        'formulario_whois': formulario_whois,
        'pais_actual': pais_actual,
    }

    response = render_to_response('accounts/dashboard.html', ctx, context_instance=RequestContext(request))
    return response

# vista para editar el perfil de usuario
@login_required(login_url='/')
def edit_user_profile_view(request):
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
    #max_age = 365*24*60*60 # 1 año

    ###############################

    msg_error = msg_ok = ''
    state = 1
    country = 1
    profile_sent = False

    if request.user.is_authenticated():
        user = User.objects.get(pk=request.user.id)
        profile = UserProfile.objects.get(user=user)
        points = PointByScore(request)

        if request.POST:
            form_user = ProfileForm(request.POST, instance=user)
            form_profile = EditRegisterForm(request.POST, instance=profile)

            if form_user.is_valid():
                if form_profile.is_valid():
                    password = form_user.cleaned_data['password']
                    repassword = form_user.cleaned_data['repassword']

                    state_id = form_profile.cleaned_data['state'].id_state
                    country_id = form_profile.cleaned_data['country'].id_country
                    language_id = form_profile.cleaned_data['language'].id_language

                    '''
					try:
						User.objects.get(email=email)
						message = 'Error: El Email ya se encuentra registrado.'
						#<a href="/forgot_pass/">¿Olvidó su contraseña?</a>

					except User.DoesNotExist:
					'''
                    addUser = form_user.save(commit=False)

                    if password:
                        if password == repassword:
                            addUser.set_password(password)

                    addUser.save()

                    addProfile = form_profile.save(commit=False)
                    addProfile.user = addUser
                    addProfile.save()
                    form_profile.save_m2m()

                    msg_ok = 'Tu perfil ha sido actualizado.'

                    profile_sent = True
        else:
            form_user = ProfileForm(instance=user)
            form_profile = EditRegisterForm(instance=profile)
    else:
        return HttpResponseRedirect('/')

    pais_actual = Country.objects.all().get(id_country=country_id)
    category = Category.objects.all().filter(status=True, type=1).order_by('title')

    # enviamos el ID del pais de la cookie
    formulario_whois = WhoisForm(initial={'Country': country_id})

    ctx = {
        'points': points,
        'email': user.email,
        'state': profile.state_id,
        'profile_sent': profile_sent,
        'msg_ok': msg_ok,
        'msg_error': msg_error,
        'profile': profile,
        'form_user': form_user,
        'form_profile': form_profile,
        'formulario_whois': formulario_whois,
        'pais_actual': pais_actual,
    }

    '''
	t = loader.get_template('accounts/profile.html')
	c = RequestContext(request, ctx)

	response = HttpResponse(t.render(c))
	response.set_cookie('gm_country', country_id, max_age=max_age, expires=today, path='/', domain=None, secure=None, httponly=False)
	response.set_cookie('gm_state', state_id, max_age=max_age, expires=today, path='/', domain=None, secure=None, httponly=False)
	response.set_cookie('gm_language', language_id, max_age=max_age, expires=today, path='/', domain=None, secure=None, httponly=False)

	return response
	'''
    response = render_to_response('accounts/profile.html', ctx, context_instance=RequestContext(request))
    response.set_cookie("gm_state", state_id)
    response.set_cookie("gm_country", country_id)
    response.set_cookie("gm_language", language_id)
    return response

# vista para listar Mis Reservaciones
@login_required(login_url='/')
def list_user_reservation_view(request, page):
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
    category = Category.objects.all().filter(status=True, type=1).order_by('title')

    message = ''
    profile_sent = False

    if request.user.is_authenticated():
        user = User.objects.get(pk=request.user.id)
        profile = UserProfile.objects.get(user=user)

        points = PointByScore(request)

        reservations = Reserve.objects.filter(user=user).order_by('status', 'date', 'time')

        # paginar los resultados a '10' por pagina
        paginator = Paginator(reservations, 10)
        try:
            num_page = int(page)
        except:
            num_page = 1
        try:
            reservations = paginator.page(num_page)
        except (EmptyPage, InvalidPage):
            reservations = paginator.page(paginator.num_pages)
    else:
        return HttpResponseRedirect('/')

    # enviamos el ID del pais de la cookie
    formulario_whois = WhoisForm(initial={'Country': country_id})

    ctx = {
        'points': points,
        'list_reservations': reservations,
        'formulario_whois': formulario_whois,
        'pais_actual': pais_actual,
    }

    response = render_to_response('accounts/reservation/my.html', ctx, context_instance=RequestContext(request))
    return response

# vista para Editar una Reservacion
@login_required(login_url='/')
def edit_user_reservation(request, id_reservation):
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
    is_dir_user = False

    if request.user.is_authenticated():
        try:
            reservation = Reserve.objects.get(pk=id_reservation, user=request.user.id)
            directory = Directory.objects.get(pk=reservation.directory.pk, status=True)

            if directory.user == request.user.id:
                is_dir_user = True

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

                    add_reserve.date_create = datetime.now().replace(tzinfo=utc)
                    add_reserve.date_update = datetime.now().replace(tzinfo=utc)

                    add_reserve.save()

                    form_sent = True
            else:
                form_reserve = ReserveForm(instance=reservation)
                form_reserve.fields['email'].widget.attrs['readonly'] = True

        except:
            return HttpResponseRedirect('/accounts/my-reservations/1/')

    else:
        return HttpResponseRedirect('/')

    # enviamos el ID del pais de la cookie
    formulario_whois = WhoisForm(initial={'Country': country_id})

    ctx = {
        'is_dir_user': is_dir_user,
        'points': points,
        'form_sent': form_sent,
        'form_reserve': form_reserve,
        'directory': directory,
        'formulario_whois': formulario_whois,
        'pais_actual': pais_actual,
    }

    response = render_to_response('accounts/reservation/edit.html', ctx, context_instance=RequestContext(request))
    return response


# vista para Cancelar una Reservacion
@login_required(login_url='/')
def cancel_user_reservation_view(request, id_reservation):
    try:
        user = User.objects.get(pk=request.user.id)

        cancel = Reserve.objects.get(pk=id_reservation, user=user)
        cancel.status = 2
        cancel.save()
    except:
        error = True

    return HttpResponseRedirect('/accounts/my-reservations/1/')

# vista para mostrar los Referidos y el link
@login_required(login_url='/')
def view_referer_view(request):
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
    category = Category.objects.all().filter(status=True, type=1).order_by('title')

    message = ''
    profile_sent = False

    if request.user.is_authenticated():
        user = User.objects.get(pk=request.user.id)
        profile = UserProfile.objects.get(user=user)

        points = PointByScore(request)

    else:
        return HttpResponseRedirect('/')

    # enviamos el ID del pais de la cookie
    formulario_whois = WhoisForm(initial={'Country': country_id})

    ctx = {
        'points': points,
        'list_user': user,
        'URL_SITE': settings.URL_SITE,
        'formulario_whois': formulario_whois,
        'pais_actual': pais_actual,
    }

    response = render_to_response('accounts/referer.html', ctx, context_instance=RequestContext(request))
    return response