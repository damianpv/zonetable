# -*- coding: utf-8 -*-
from django import forms
from django.forms.fields import DateField
from django.forms.extras.widgets import SelectDateWidget

from zonetable.apps.home.models import State, Country, Language
from zonetable.apps.directory.models import Category, Service, Payment, Currency, Style, Directory, Package, Pay

SELECCIONE_CHOICES = (
    ('', 'Seleccione uno'),
)

HORA_CHOICES = (
    ('12:00 AM', '12:00 AM'), ('12:30 AM', '12:30 AM'), ('01:00 AM', '01:00 AM'), ('01:30 AM', '01:30 AM'),
    ('02:00 AM', '02:00 AM'), ('02:30 AM', '02:30 AM'), ('03:00 AM', '03:00 AM'), ('03:30 AM', '03:30 AM'),
    ('04:00 AM', '04:00 AM'), ('04:30 AM', '04:30 AM'), ('05:00 AM', '05:00 AM'), ('05:30 AM', '05:30 AM'),
    ('06:00 AM', '06:00 AM'), ('06:30 AM', '06:30 AM'), ('07:00 AM', '07:00 AM'), ('07:30 AM', '07:30 AM'),
    ('08:00 AM', '08:00 AM'), ('08:30 AM', '08:30 AM'), ('09:00 AM', '09:00 AM'), ('09:30 AM', '09:30 AM'),
    ('10:00 AM', '10:00 AM'), ('10:30 AM', '10:30 AM'), ('11:00 AM', '11:00 AM'), ('11:30 AM', '11:30 AM'),

    ('12:00 PM', '12:00 PM'), ('12:30 PM', '12:30 PM'), ('01:00 PM', '01:00 PM'), ('01:30 PM', '01:30 PM'),
    ('02:00 PM', '02:00 PM'), ('02:30 PM', '02:30 PM'), ('03:00 PM', '03:00 PM'), ('03:30 PM', '03:30 PM'),
    ('04:00 PM', '04:00 PM'), ('04:30 PM', '04:30 PM'), ('05:00 PM', '05:00 PM'), ('05:30 PM', '05:30 PM'),
    ('06:00 PM', '06:00 PM'), ('06:30 PM', '06:30 PM'), ('07:00 PM', '07:00 PM'), ('07:30 PM', '07:30 PM'),
    ('08:00 PM', '08:00 PM'), ('08:30 PM', '08:30 PM'), ('09:00 PM', '09:00 PM'), ('09:30 PM', '09:30 PM'),
    ('10:00 PM', '10:00 PM'), ('10:30 PM', '10:30 PM'), ('11:00 PM', '11:00 PM'), ('11:30 PM', '11:30 PM'),
)

PAY_MONTH_CHOICES = (
    ('1', '1'), ('6', '6'),  ('12', '12'),
)

COMENTARIOS_CHOICES = (('0', 'No',), ('1', 'Sí',))

class addRestaurantForm(forms.ModelForm):
    title           = forms.CharField(widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'1','placeholder':u'Inserte el Título...', 'autofocus':'autofocus'}), error_messages={'required': 'Campo obligatorio', 'unique': u'Ya existe.'})
    address         = forms.CharField(widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'2','placeholder':u'Inserte la Dirección...'}), error_messages={'required': 'Campo obligatorio'})
    postal_code     = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'input-xlarge', 'maxlength':'5', 'tabindex':'3','placeholder':u'Inserte el Código Postal...'}))
    city            = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'4','placeholder':u'Inserte la Ciudad...'}))
    state           = forms.ModelChoiceField(queryset = State.objects.all().filter(status=True), widget=forms.Select(attrs={'style': u'width: 250px'}), error_messages={'required': 'Campo obligatorio'})
    country         = forms.ModelChoiceField(queryset = Country.objects.all().filter(status=True), widget=forms.Select(attrs={'style': u'width: 250px'}), error_messages={'required': 'Campo obligatorio'})
    language        = forms.ModelChoiceField(queryset = Language.objects.all().filter(status=True), widget=forms.Select(attrs={'style': u'width: 250px'}), error_messages={'required': 'Campo obligatorio'})
    category        = forms.ModelMultipleChoiceField(queryset=Category.objects.all().filter(status=True), widget=forms.SelectMultiple(attrs={'placeholder': u'Seleccione el/los tipos de comida'}), error_messages={'required': 'Campo obligatorio'})
    style           = forms.ModelMultipleChoiceField(queryset=Style.objects.all().filter(status=True).order_by('title'), widget=forms.SelectMultiple(attrs={'placeholder': u'Seleccione el/los estilo de vestir'}), error_messages={'required': 'Campo obligatorio'})
    service         = forms.ModelMultipleChoiceField(required=False, queryset=Service.objects.all().filter(status=True).order_by('title'), widget=forms.SelectMultiple(attrs={'placeholder': u'Seleccione el/los servicios disponibles'}))
    payment         = forms.ModelMultipleChoiceField(queryset=Payment.objects.all().filter(status=True).order_by('title'), widget=forms.SelectMultiple(attrs={'placeholder': u'Seleccione la(s) formas de pago'}), error_messages={'required': 'Campo obligatorio'})
    currency        = forms.ModelChoiceField(queryset = Currency.objects.all().filter(status=True).order_by('title'), widget=forms.Select(attrs={'style': u'width: 250px'}), error_messages={'required': 'Campo obligatorio'})
    #horario         = forms.CharField(widget=forms.Select(choices=HORA_CHOICES, attrs={'tabindex':'7','style':'width:100px'}))
    phone           = forms.CharField(widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'8','placeholder':u'Inserte el Teléfono...'}), error_messages={'required': 'Campo obligatorio'})
    cell            = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'9','placeholder':u'Inserte el Celular...'}), error_messages={'required': 'Campo obligatorio'})
    email           = forms.EmailField(widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'10','placeholder':'Inserte su Email...'}), error_messages={'required': 'Campo obligatorio'})
    website         = forms.URLField(required=False, widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'10','placeholder':'Inserte su Sitio Web...'}), error_messages={'required': 'Campo obligatorio'})
    twitter         = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'span2 input-xlarge', 'tabindex':'10','placeholder':'Inserte su cuenta de Twitter...'}))
    facebook        = forms.URLField(required=False, widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'10','placeholder':'Inserte su URL de Facebook...'}))
    google_plus     = forms.URLField(required=False, widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'10','placeholder':'Inserte su URL de Google Plus...'}))
    description     = forms.CharField(widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'10','placeholder':'Inserte la Descripción en 255 caracteres...'}), error_messages={'required': 'Campo obligatorio'})
    keywords        = forms.CharField(widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'10','placeholder':'Inserte las Palabras Claves (separe por coma ",")...'}), error_messages={'required': 'Campo obligatorio'})
    content         = forms.CharField(required=False, widget=forms.widgets.Textarea(attrs={'cols': 10, 'rows': 20}))
    #comment        = forms.ChoiceField(widget=forms.RadioSelect, choices=COMENTARIOS_CHOICES, initial='1')
    logo            = forms.ImageField(required=False)
    geo_location    = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'input-xxlarge','style': 'display:none;', 'tabindex':'10'}))

    class Meta:
        model = Directory
        #fields=('country','state')
        exclude = {'status', 'user', 'url_name', 'google_plus', 'date_create', 'date_update'}


'''
class CreateRestaurantForm(forms.Form):
    titulo          = forms.CharField(widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'1','placeholder':u'Inserte el Título...', 'autofocus':'autofocus'}), error_messages={'required': 'Campo obligatorio'})
    direccion       = forms.CharField(widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'2','placeholder':u'Inserte la Dirección...'}), error_messages={'required': 'Campo obligatorio'})
    codigo_postal   = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'3','placeholder':u'Inserte el Código Postal...'}))
    ciudad          = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'4','placeholder':u'Inserte la Ciudad...'}))
    estado          = forms.ModelChoiceField(queryset = State.objects.all().filter(status=True), widget=forms.Select(attrs={'style': u'width: 250px'}))
    pais            = forms.ModelChoiceField(queryset = Country.objects.all().filter(status=True), widget=forms.Select(attrs={'style': u'width: 250px'}))

    categoria       = forms.ModelMultipleChoiceField(queryset=Category.objects.all().filter(status=True), widget=forms.SelectMultiple(attrs={'placeholder': u'Inserte ...'}), error_messages={'required': 'Campo obligatorio'})

    horario         = forms.CharField(widget=forms.Select(choices=HORA_CHOICES, attrs={'tabindex':'7','style':'width:100px'}))
    telefono        = forms.CharField(widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'8','placeholder':u'Inserte el Teléfono...'}), error_messages={'required': 'Campo obligatorio'})
    celular         = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'9','placeholder':u'Inserte el Celular...'}), error_messages={'required': 'Campo obligatorio'})
    email           = forms.EmailField(widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'10','placeholder':'Inserte su Email...'}), error_messages={'required': 'Campo obligatorio'})
    sitio_web       = forms.URLField(required=False, widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'10','placeholder':'Inserte su Sitio Web...'}), error_messages={'required': 'Campo obligatorio'})
    twitter         = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'span2 input-xlarge', 'tabindex':'10','placeholder':'Inserte su cuenta de Twitter...'}))
    facebook        = forms.URLField(required=False, widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'10','placeholder':'Inserte su URL de Facebook...'}))
    google_plus     = forms.URLField(required=False, widget=forms.TextInput(attrs={'class':'input-xlarge', 'tabindex':'10','placeholder':'Inserte su URL de Google Plus...'}))
    contenido       = forms.CharField(required=False, widget=forms.widgets.Textarea(attrs={'cols': 10, 'rows': 20}))
    comentarios     = forms.ChoiceField(widget=forms.RadioSelect, choices=COMENTARIOS_CHOICES, initial='1')
    ubicacion_gmap  = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'input-xxlarge', 'tabindex':'10'}))

    #birth_year = forms.DateField(required=False, widget=MySelectDateWidget(years=range(1980, 2013)))
'''

class PackageForm(forms.ModelForm):
    package     = forms.ModelMultipleChoiceField(queryset=Package.objects.all().filter(status=True), initial=['1', '2'], widget=forms.SelectMultiple(attrs={'style': 'display:none;'}))
    concept     = forms.CharField(widget=forms.HiddenInput(attrs={'value':'Pago'}))
    payment     = forms.ModelChoiceField(initial=0, queryset = Payment.objects.all().filter(status=True, pay_in_gm=True).order_by('title'), widget=forms.Select(attrs={'style':'width:100px'}))
    pay_months  = forms.CharField(widget=forms.Select(choices=PAY_MONTH_CHOICES, attrs={'style':'width:100px'}))
    price       = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Pay
        #fields=('country','state')
        exclude = {'status', 'user', 'email', 'pay_status', 'subtotal',
                    'pay_id', 'id_concept', 'description', 'date_create', 'date_begin', 'date_end'}
