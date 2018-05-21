# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.timezone import utc

from zonetable.apps.accounts.models import UserProfile
from zonetable.apps.directory.forms import SearchRestaurantForm
from zonetable.apps.directory.models import Category, Directory
from zonetable.apps.functions.forms import WhoisForm
from zonetable.apps.home.models import State, Country
from zonetable.apps.functions.views import PointByScore, getUserCountry

def search_rest_view(request, page):
	try:
		country_id = request.COOKIES['gm_country']
		state_id = request.COOKIES['gm_state']
		language_id = request.COOKIES['gm_language']
	except:
		remote_addr = request.META.get('HTTP_X_FORWARDED_FOR',"127.0.0.1")
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
	max_age = 90*24*60*60 # 3 meses (90 días)

	###############################

	pais_actual = Country.objects.all().get(id_country=country_id)
	category = Category.objects.all().filter(status=True, type=1, directory__isnull=False, directory__country_id=country_id, directory__deleted=False, directory__status=True).order_by('title').distinct()

	search_sent = False
	message = ''
	directory = ''

	if request.GET:
		search_sent = True
		formulario = SearchRestaurantForm(request.GET)
		formulario.fields['Estado'].queryset = State.objects.filter(country_id=country_id)

		if formulario.is_valid():
			form_nombre = formulario.cleaned_data['Nombre']
			form_category = formulario.cleaned_data['Categoria']
			form_state = formulario.cleaned_data['Estado']
			if form_category > 0:
				directory = Directory.objects.all().filter(status=True,
							title__contains=form_nombre,
							category__id_category__exact=form_category.id_category,
							state__id_state__exact=form_state.id_state).order_by('-id_directory')
			else:
				directory = Directory.objects.all().filter(status=True,
							title__contains=form_nombre,
							state__id_state__exact=form_state.id_state).order_by('-id_directory')

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
		else:
			message = 'Por favor, seleccione un criterio de búsqueda.'
	else:
		formulario = SearchRestaurantForm()
		formulario.fields['Estado'].queryset = State.objects.filter(country_id=country_id)
		message = 'Por favor, seleccione un criterio de búsqueda.'

# ?Nombre=&Fecha=2013-02-17&Hora=02%3A00+AM&Categoria=&Personas=1+Persona&Estado=59

	# enviamos el ID del pais de la cookie
	formulario_whois = WhoisForm(initial={'Country':country_id})

	ctx = {
		'points':points,
		'form_rest':formulario,
		'formulario_whois':formulario_whois,
		'list_category':category,
		'list_directory':directory,
		'pais_actual':pais_actual,
		'message':message,

		#'nombre':formulario.cleaned_data['Nombre'],
		#'fecha':formulario.cleaned_data['Fecha'],
		#'hora':formulario.cleaned_data['Hora'],
		#'categoria':formulario.cleaned_data['Categoria'],
		#'personas':formulario.cleaned_data['Personas'],
		#'estado':formulario.cleaned_data['Estado'].id_state,
	}

	response = render_to_response('search/search_rest.html', ctx, context_instance=RequestContext(request))
	response.set_cookie("gm_state", state_id)
	response.set_cookie("gm_country", country_id)
	response.set_cookie("gm_language", language_id)
	return response