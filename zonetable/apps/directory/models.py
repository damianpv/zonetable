from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils.timezone import utc
from datetime import datetime, timedelta
#import random

from zonetable.apps.home.models import State, Country, Language

# Modelo para Categorias del directorio
class Category(models.Model):
	id_category = models.AutoField(primary_key=True)
	status = models.BooleanField(default=False)
	title = models.CharField(max_length=100)
	type = models.CharField(max_length=1)
	url_name = models.SlugField(max_length=100)

	def __unicode__(self):
		return self.title

# Modelo para Servicios del Directorio
class Service(models.Model):
	id_service = models.AutoField(primary_key=True)
	status = models.BooleanField(default=False)
	title = models.CharField(max_length=50)

	def __unicode__(self):
		return self.title

# Modelo para Formas de Pagos del Directorio
class Payment(models.Model):
	id_service 	= models.AutoField(primary_key=True)
	status 		= models.BooleanField(default=False)
	title 		= models.CharField(max_length=50)
	initials 	= models.CharField(max_length=10)
	pay_in_gm 	= models.BooleanField(default=False)

	def __unicode__(self):
		return self.title

# Modelo para Moneda del Directorio
class Currency(models.Model):
	id_currency = models.AutoField(primary_key=True)
	status = models.BooleanField(default=False)
	title = models.CharField(max_length=50)

	def __unicode__(self):
		return self.title

# Modelo para Estilo del Directorio
class Style(models.Model):
	id_style = models.AutoField(primary_key=True)
	status = models.BooleanField(default=False)
	title = models.CharField(max_length=50)

	def __unicode__(self):
		return self.title

# Modelo para Directorio de fichas
class Directory(models.Model):

	def url(self,filename):
		ruta = "directory/logo/%s_%s" % (self.user.pk, str(filename))
		return ruta

	id_directory = models.AutoField(primary_key=True)
	status = models.BooleanField(default=False)
	deleted = models.BooleanField(default=False)
	title = models.CharField(max_length=100)
	address = models.CharField(max_length=100)
	postal_code = models.CharField(max_length=5, null=True, blank=True)
	city = models.CharField(max_length=100, null=True, blank=True)
	state = models.ForeignKey(State)
	country = models.ForeignKey(Country)
	language = models.ForeignKey(Language)
	category = models.ManyToManyField(Category)
	service = models.ManyToManyField(Service, blank=True, null=True)
	payment = models.ManyToManyField(Payment)
	currency = models.ForeignKey(Currency)
	style = models.ManyToManyField(Style)
	phone = models.CharField(max_length=45, null=True)
	cell = models.CharField(max_length=45, null=True, blank=True)
	email = models.EmailField(max_length=100, null=True, blank=True)
	email_user = models.BooleanField(default=True)
	website = models.CharField(max_length=100, null=True, blank=True)
	description = models.CharField(max_length=255)
	keywords = models.CharField(max_length=255)
	content = models.TextField(null=True)
	comment = models.BooleanField(default=True)
	logo = models.ImageField(upload_to=url, null=True, blank=True)
	geo_location = models.CharField(max_length=50, null=True, blank=True)
	twitter = models.CharField(max_length=50, null=True, blank=True)
	facebook = models.CharField(max_length=100, null=True, blank=True)
	google_plus = models.CharField(max_length=100, null=True, blank=True)
	url_name = models.SlugField(max_length=255, error_messages={'unique':"Ya existe."}, null=True, blank=True)
	user = models.ForeignKey(User)
	date_create = models.DateTimeField()
	date_update = models.DateTimeField()
	need_reservation = models.BooleanField(default=False)

	def save(self, *args, **kwargs):
		url_name = slugify(self.title)
		random_number = User.objects.make_random_password(length=3, allowed_chars='123456789')

		#try:
		#	d = Directory.objects.get(url_name=url_name) #, pk__icontains=id_directory
		#	self.url_name = url_name + '-' + random_number
		#	super(Directory, self).save(*args, **kwargs)
		#except:
		self.url_name = url_name
		super(Directory, self).save(*args, **kwargs)

	def __unicode__(self):
		return u"%s (%s)" % (self.title, u", ".join([category.title
                                                    for category in self.category.all()]))

# Modelo para los Horarios de las fichas
class Hours(models.Model):
	id_hours = models.AutoField(primary_key=True)
	status = models.BooleanField(default=True)
	directory = models.ForeignKey(Directory)
	day_week = models.CharField(max_length=2)
	hour_in = models.CharField(max_length=5)
	hour_out = models.CharField(max_length=5)

	def __unicode__(self):
		return self.day_week

# Modelo para las Estadisticas de las fichas
class Stat(models.Model):
	id_stat = models.AutoField(primary_key=True)
	directory = models.ForeignKey(Directory)
	date = models.DateField()
	count = models.CharField(max_length=10)

	def __unicode__(self):
		return self.date

# Modelo para las Reservaciones
class Reserve(models.Model):
	id_reserve	= models.AutoField(primary_key=True)
	status 		= models.IntegerField(default=0)
	type		= models.IntegerField(default=0) # 0: reservar mesa, 1: a domicilio.
	directory 	= models.ForeignKey(Directory, related_name='+')
	user 		= models.ForeignKey(User, blank=True, null=True)
	name 		= models.CharField(max_length=100, blank=True, null=True)
	email 		= models.EmailField(max_length=100, blank=True, null=True)
	phone 		= models.CharField(max_length=100, blank=True, null=True)
	people 		= models.IntegerField(max_length=2)
	date 		= models.DateField(blank=True, null=True)
	time 		= models.TimeField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	score 		= models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
	point 		= models.IntegerField(max_length=4, blank=True, null=True)
	date_create = models.DateTimeField()
	date_update = models.DateTimeField()

	def __unicode__(self):
		return self.email

# Modelo para los Comentarios de las fichas
class Comment(models.Model):
	id_comment	= models.AutoField(primary_key=True)
	status 		= models.BooleanField(default=False)
	directory 	= models.ForeignKey(Directory, related_name='+')
	user 		= models.ForeignKey(User, blank=True, null=True)
	name 		= models.CharField(max_length=100, blank=True, null=True)
	email 		= models.EmailField(max_length=100)
	comment 	= models.TextField(blank=True, null=True)
	date_create = models.DateTimeField()

	def __unicode__(self):
		return self.email

# Modelo para Votar / Calificar las fichas
class Rate(models.Model):
	id_rate		= models.AutoField(primary_key=True)
	directory 	= models.ForeignKey(Directory, related_name='+')
	value 		= models.IntegerField(max_length=1)
	date_create = models.DateTimeField(null=True, blank=True)

	def __unicode__(self):
		return self.value


# Modelo para seleccionar los Paquetes para el pago
class Package(models.Model):
	id_package 	= models.AutoField(primary_key=True)
	status 		= models.BooleanField(default=False)
	title		= models.CharField(max_length=100)
	content 	= models.TextField()
	price		= models.DecimalField(max_digits=5, decimal_places=2)
	order		= models.IntegerField(max_length=2, default=0)
	date_create = models.DateTimeField()

	def __unicode__(self):
		return self.title

# Modelo para registrar los Pagos de los establecimientos
class Pay(models.Model):
	id_pay 		= models.AutoField(primary_key=True)
	user 		= models.ForeignKey(User)
	package 	= models.ManyToManyField(Package)
	payment		= models.ForeignKey(Payment)
	directory 	= models.ForeignKey(Directory, null=True, blank=True)
	pay_status	= models.IntegerField(default=1)
	txn_id		= models.CharField(max_length=50, null=True, blank=True)
	receiver_id	= models.CharField(max_length=50, null=True, blank=True)
	subtotal	= models.CharField(max_length=10, null=True, blank=True)
	pay_months	= models.IntegerField(max_length=5)
	price		= models.CharField(max_length=10, null=True, blank=True)
	concept		= models.CharField(max_length=100)
	date_create = models.DateTimeField()
	date_begin 	= models.DateTimeField()
	date_end 	= models.DateTimeField()

	def save(self, *args, **kwargs):
		'''
		try:
			d = Pay.objects.get(pk=id_pay) #, pk__icontains=id_directory
			self.date_end = datetime.now().replace(tzinfo=utc)+timedelta(days=self.pay_months)
			super(Pay, self).save(*args, **kwargs)
		except:
		'''
		self.concept = 'Pago %s Mes(es)' % (self.pay_months)
		self.date_end = datetime.now().replace(tzinfo=utc)+timedelta(days=(self.pay_months + 1) * 30)
		super(Pay, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.concept
