from django.core import serializers
from django.http import HttpResponse
from django.db import models
from django.contrib.auth.models import User

# Modelo para idioma
class Language(models.Model):
	id_language = models.AutoField(primary_key=True)
	status = models.BooleanField(default=True)
	language = models.CharField(max_length=45)

	def __unicode__(self):
		return self.language

# Modelo para Pais
class Country(models.Model):
	id_country = models.AutoField(primary_key=True)
	status = models.BooleanField(default=True)
	country = models.CharField(max_length=45)
	fips104 = models.CharField(max_length=7)
	iso2 = models.CharField(max_length=4)
	iso3 = models.CharField(max_length=4)
	ison = models.CharField(max_length=4)
	internet = models.CharField(max_length=8)
	capital = models.CharField(max_length=20)
	map_ref = models.CharField(max_length=50)
	nac_singular = models.CharField(max_length=30)
	nac_plural = models.CharField(max_length=30)
	currency = models.CharField(max_length=30)
	currency_code = models.CharField(max_length=12)
	population = models.CharField(max_length=10)
	title = models.CharField(max_length=50)
	comment = models.CharField(max_length=50)

	def __unicode__(self):
		return self.country

# Modelo para Estado
class State(models.Model):
	id_state = models.AutoField(primary_key=True)
	status = models.BooleanField(default=True)
	country = models.ForeignKey(Country)
	state = models.CharField(max_length=45)
	code = models.CharField(max_length=4)
	adm1code = models.CharField(max_length=8)

	def __unicode__(self):
		return self.state

# Modelo para Ciudad
class City(models.Model):
	id_city = models.AutoField(primary_key=True)
	status = models.BooleanField(default=True)
	country = models.ForeignKey(Country)
	state = models.ForeignKey(State)
	city = models.CharField(max_length=45)
	latitude = models.CharField(max_length=10, null=True, blank=True)
	longitude = models.CharField(max_length=10, null=True, blank=True)
	timezone = models.CharField(max_length=10, null=True, blank=True)
	dmald = models.CharField(max_length=5, null=True, blank=True)
	code = models.CharField(max_length=6, null=True, blank=True)

	def __unicode__(self):
		return self.city

#########################################################

# Modelo para Contacto
class Contact(models.Model):
	id_contact = models.AutoField(primary_key=True)
	status = models.BooleanField(default=True)
	name = models.CharField(max_length=45)
	email = models.CharField(max_length=45)
	phone = models.CharField(max_length=45, null=True)
	language = models.ForeignKey(Language)
	country = models.ForeignKey(Country)
	how_know = models.CharField(max_length=45)
	subject = models.CharField(max_length=45)
	content = models.TextField()
	date_create = models.DateTimeField()

	def __unicode__(self):
		return self.email

# Modelo para contenido
class Content(models.Model):
	id_content = models.AutoField(primary_key=True)
	status = models.BooleanField(default=True)
	title = models.CharField(max_length=45)
	content = models.TextField(null=True)
	url_name = models.CharField(max_length=45)
	country = models.ForeignKey(Country)
	language = models.ForeignKey(Language)
	date_create = models.DateTimeField()

	def __unicode__(self):
		return self.title

# Modelo para newsletter
class Newsletter(models.Model):
	id_newsletter = models.AutoField(primary_key=True)
	status = models.BooleanField(default=True)
	email = models.CharField(max_length=45)
	country = models.ForeignKey(Country)
	language = models.ForeignKey(Language)
	date_create = models.DateTimeField()

	def __unicode__(self):
		return self.email

'''
class producto(models.Model):

	def url(self,filename):
		ruta = "MultimediaData/Producto/%s/%s"%(self.nombre,str(filename))
		return ruta


	nombre		= models.CharField(max_length=100)
	descripcion	= models.TextField(max_length=300)
	status		= models.BooleanField(default=True)
	imagen 		= models.ImageField(upload_to=url,null=True,blank=True)
	precio		= models.DecimalField(max_digits=6,decimal_places=2)
	stock		= models.IntegerField()

	def __unicode__(self):
		return self.nombre
'''

# Modelo para recomendar
class Recommend(models.Model):
	id_recommend = models.AutoField(primary_key=True)
	status = models.BooleanField(default=True)
	name_remitter = models.CharField(max_length=45)
	email_remitter = models.CharField(max_length=45)
	name_receiver1 = models.CharField(max_length=45)
	email_receiver1 = models.CharField(max_length=45)
	name_receiver2 = models.CharField(max_length=45, null=True)
	email_receiver2 = models.CharField(max_length=45, null=True)
	name_receiver3 = models.CharField(max_length=45, null=True)
	email_receiver3 = models.CharField(max_length=45, null=True)
	content = models.TextField()
	language = models.ForeignKey(Language)
	date_create = models.DateTimeField()

	def __unicode__(self):
		return self.email_remitter