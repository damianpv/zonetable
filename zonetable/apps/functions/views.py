# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import EmailMultiAlternatives # Enviamos HTML
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.db.models import Sum


from urllib2 import urlopen, Request
import re, socket

domain_re = re.compile('^(http|https):\/\/?([^\/]+)')
domain = domain_re.match('http://www.google.com').group(2)

from zonetable.apps.functions.forms import WhoisForm
from zonetable.apps.directory.models import Reserve
from zonetable.apps.home.models import Country

#from zonetable.apps.home.models import Contacto
#from zonetable.apps.home.models import Contenido
#from zonetable.apps.home.forms import ContactForm
#from zonetable.apps.accounts.forms import LoginForm
#from zonetable.apps.directory.models import Directorio

from datetime import datetime

def whois_set_view(request):
	content = ''

	if request.POST:
		form = WhoisForm(request.POST)
		if form.is_valid():
			country = form.cleaned_data['Country']
			language = form.cleaned_data['Language']
			state = 1

			today = datetime.now()
			today = today.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
			max_age = 90*24*60*60 # 3 meses (90 días)
			#max_age = 365*24*60*60 # 1 año

			#expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")

			'''
			response = HttpResponse()
			response.set_cookie("gm_state", state)
			response.set_cookie("gm_country", country.id_country)
			response.set_cookie("gm_language", language)

			response.set_cookie('gm_country', country.id_country, max_age=max_age, expires=today, path='/', domain=None, secure=None, httponly=False)
			response.set_cookie('gm_state', state, max_age=max_age, expires=today, path='/', domain=None, secure=None, httponly=False)
			response.set_cookie('gm_language', language, max_age=max_age, expires=today, path='/', domain=None, secure=None, httponly=False)
			'''

			ctx = {
				'content': 0,
			}

			response = render_to_response('functions/content.html', ctx, context_instance=RequestContext(request))
			response.set_cookie("gm_state", state)
			response.set_cookie("gm_country", country.id_country)
			response.set_cookie("gm_language", language)
			return response

	'''
			#return HttpResponse("Your favorite color is %s" % request.COOKIES["favorite_color"])

			#request.COOKIES["favorite_color"]
			content = 'ok'
	ctx = {
		'content': content,
		'response':response
	}

	return render_to_response('functions/content.html',ctx)
	'''

def whois_get_view(request):
	try:
		country = request.COOKIES['gm_country']
		language = request.COOKIES['gm_language']
		state = request.COOKIES['gm_state']

		content = 1
	except:
		content = 0

	ctx = {
		'content': content,
	}
	return render_to_response('functions/content.html', ctx)

# funcion para el envio de correos usando un template
def send_mail(email_from, email_to, subject, content, page_url, headers):
	subject, from_email, to = subject, email_from, email_to
	html_content = render_to_string('email/%s' % (page_url), {'content':content}) # HTML generate
	text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.
	# create the email, and attach the HTML version as well.

	#headers = {'Cc': headers}

	msg = EmailMultiAlternatives(subject, text_content, from_email, [to], headers=headers)
	msg.attach_alternative(html_content, "text/html")
	msg.send()

# Calculamos el total de puntos de un usuario
# Se calcula por el total consumido en la reservacion
# Se le resta puntos consumidos
def PointByScore(request):

	points = total_points = 0
	total_score = Reserve.objects.all().filter(status=4, user=request.user.id).aggregate(score=Sum('score'))
	total_point = Reserve.objects.all().filter(status=4, user=request.user.id).aggregate(point=Sum('point'))

	try:
		total_points = int(total_point['point'])
	except TypeError:
		total_points = 0

	try:
		points = ((total_score['score'] * 5) / 100) - total_points
	except TypeError:
		points = 0

	return int(round(points))

#obtener el pais segun la IP del usuario
def getUserCountry(ip):
    ip = ip.split(', ')
    url = "http://api.wipmania.com/" + ip[len(ip)-1] + "?" + domain
    socket.setdefaulttimeout(5)
    headers = {'Typ':'django','Ver':'1.0','Connection':'Close'}
    try:
        req = Request(url, None, headers)
        urlfile = urlopen(req)
        land = urlfile.read()
        urlfile.close()

        country = Country.objects.get(fips104=land[:2])

        return country.pk
    except Exception:
        return "1"
