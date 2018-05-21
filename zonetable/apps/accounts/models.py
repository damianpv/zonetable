# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import utc
from datetime import datetime
from django.conf import settings

from zonetable.apps.home.models import Language, State, Country
from zonetable.apps.directory.models import Category
from zonetable.apps.functions.views import send_mail

class UserProfile(models.Model):
	user 			 = models.ForeignKey(User, unique=True)
    #user 			 = models.OneToOneField(User)
	address 		 = models.CharField(max_length=100, null=True, blank=True)
	phone 			 = models.CharField(max_length=45, null=True, blank=True)
	birth_day 		 = models.CharField(max_length=2, null=True, blank=True)
	birth_month 	 = models.CharField(max_length=2, null=True, blank=True)
	birth_year 		 = models.CharField(max_length=4, null=True, blank=True)
	state 			 = models.ForeignKey(State)
	country 		 = models.ForeignKey(Country)
	language 		 = models.ForeignKey(Language)
	random 			 = models.CharField(max_length=10, null=True, blank=True)
	user_status 	 = models.BooleanField(max_length=1, default=False)
	fb_id 			 = models.CharField(max_length=50, null=True, blank=True)
	fb_verify 		 = models.BooleanField(max_length=1, default=False)
	gender 			 = models.CharField(max_length=10, null=True, blank=True)
	locale 			 = models.CharField(max_length=10, null=True, blank=True)
	birthday 		 = models.CharField(max_length=10, null=True, blank=True)
	category 		 = models.ManyToManyField(Category)
	newsletter 		 = models.BooleanField(max_length=1, default=True)
	terms_conditions = models.BooleanField(max_length=1, default=False)
	referer			 = models.IntegerField(max_length=11, null=True, blank=True)

	def __unicode__(self):
		return self.user.username

class Recommendation(models.Model):
	status 	= models.BooleanField(default=False)
	name 	= models.CharField(max_length=100)
	email 	= models.EmailField(max_length=50)
	user 	= models.ForeignKey(User, null=True, blank=True)
	date 	= models.DateTimeField(null=True, blank=True)

	def save(self, *args, **kwargs):

		email_to = self.email
		name = self.name

		try:
			d = Recommendation.objects.get(email=email_to)
		except Recommendation.DoesNotExist:
			self.email = email_to
			self.name = name
			self.date = datetime.now().replace(tzinfo=utc)
			super(Recommendation, self).save(*args, **kwargs)

			#enviar Email
			email_from = settings.EMAIL_FROM
			subject = 'ZoneTable - Recomendación'
			page_url = 'recommendation_admin.html'
			content = '<p>Estimado <strong>%s</strong>:</p>' % (name)
			content += '<p>Nos ponemos en contacto con usted para recomendarle visite <a href="%s">ZoneTable.com</a></p>' % (settings.URL_SITE)
			content += '<p></p>'
			content += '<p><strong>Qu&eacute; es ZoneTable?</strong></p>'
			content += '<p></p>'
			content += '<p><a href="%s">ZoneTable.com</a> est&aacute; dirigido a Restaurantes, Caf&eacute;s, Bares, entre otros. Ponemos a su disposici&oacute;n herramientas para promocionar su <strong>Establecimiento</strong>.</p>' % (settings.URL_SITE)
			content += '<p></p>'
			content += '<p><strong>Nuestros principales servicios:</strong></p>'
			content += '<p></p>'
			content += '<p>- Informaci&oacute;n detallada de su Establecimiento.</p>'
			content += '<p>- Reservas en l&iacute;nea.</p>'
			content += '<p>- Administrador de reservaciones.</p>'
			content += '<p>- Tus clientes participan en el programa de puntos comensales.</p>'
			content += '<p></p>'
			content += '<p>Para m&aacute;s informaci&oacute;n, conoce como <a href="%saffiliate/">Afiliar Establecimiento en ZoneTable.com</a>.</p>' % (settings.URL_SITE)
			content += '<p></p>'
			content += '<p>Cualquier duda o comentario no dude en <a href="%scontact/">contactarnos</a>.</p>' % (settings.URL_SITE)
			content += '<br />'
			content += '<p>Te esperamos,</p>'

			send_mail(email_from, email_to, subject, content, page_url, headers=None)

			send_mail(email_from, email_from, subject, content, page_url, headers=None)


	def __unicode__(self):
		return self.email
