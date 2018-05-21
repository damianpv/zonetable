# -*- coding: utf-8 -*-

from django import forms
import datetime

from zonetable.apps.home.models import State, Country
from zonetable.apps.directory.models import Category, Hours, Reserve, Comment, Rate

TODOS_CHOICES = (
    ('0', 'Todos'),
)

HORA_CHOICES = (
    ('', 'Seleccione'),
    ('00:00:00', '12:00 AM'), ('00:30:00', '12:30 AM'), ('01:00:00', '01:00 AM'), ('01:30:00', '01:30 AM'),
    ('02:00:00', '02:00 AM'), ('02:30:00', '02:30 AM'), ('03:00:00', '03:00 AM'), ('03:30:00', '03:30 AM'),
    ('04:00:00', '04:00 AM'), ('04:30:00', '04:30 AM'), ('05:00:00', '05:00 AM'), ('05:30:00', '05:30 AM'),
    ('06:00:00', '06:00 AM'), ('06:30:00', '06:30 AM'), ('07:00:00', '07:00 AM'), ('07:30:00', '07:30 AM'),
    ('08:00:00', '08:00 AM'), ('08:30:00', '08:30 AM'), ('09:00:00', '09:00 AM'), ('09:30:00', '09:30 AM'),
    ('10:00:00', '10:00 AM'), ('10:30:00', '10:30 AM'), ('11:00:00', '11:00 AM'), ('11:30:00', '11:30 AM'),

    ('12:00:00', '12:00 PM'), ('12:30:00', '12:30 PM'), ('13:00:00', '01:00 PM'), ('13:30:00', '01:30 PM'),
    ('14:00:00', '02:00 PM'), ('14:30:00', '02:30 PM'), ('15:00:00', '03:00 PM'), ('15:30:00', '03:30 PM'),
    ('16:00:00', '04:00 PM'), ('16:30:00', '04:30 PM'), ('17:00:00', '05:00 PM'), ('17:30:00', '05:30 PM'),
    ('18:00:00', '06:00 PM'), ('18:30:00', '06:30 PM'), ('19:00:00', '07:00 PM'), ('19:30:00', '07:30 PM'),
    ('20:00:00', '08:00 PM'), ('20:30:00', '08:30 PM'), ('21:00:00', '09:00 PM'), ('21:30:00', '09:30 PM'),
    ('22:00:00', '10:00 PM'), ('22:30:00', '10:30 PM'), ('23:00:00', '11:00 PM'), ('23:30:00', '11:30 PM'),
)

PERSONAS_CHOICES = (
    ('', 'Seleccione'),
    ('1', '1 Persona'),    ('2', '2 Personas'),   ('3', '3 Personas'), 
    ('4', '4 Personas'),   ('5', '5 Personas'),   ('6', '6 Personas'),    
    ('7', '7 Personas'),   ('8', '8 Personas'),   ('9', '9 Personas'),    
    ('10', '10 Personas'), ('11', '11 Personas'), ('12', '12 Personas'),    
    ('13', '13 Personas'), ('14', '14 Personas'), ('15', '15 Personas'),    
    ('16', '16 Personas'), ('17', '17 Personas'), ('18', '18 Personas'),    
    ('19', '19 Personas'), ('20', '20 Personas'), ('21', 'Grupo'),    
)

class SearchRestaurantForm(forms.Form):
    '''
    def __init__(self, Nombre, *args, **kwargs):
        super(RestaurantForm, self).__init__(*args, **kwargs)
        self.fields['Nombre'].queryset = State.objects.filter(country_id=Nombre)
    
    class Meta:
        model = State
    '''

    #Horario.objects.all().values_list('id_horario','hora_inicio')
    #TODOS_CHOICES = State.objects.all().values_list('id_state','state')

    Nombre  = forms.CharField(required=False, widget=forms.TextInput(attrs={'tabindex':'1','class':'input-xlarge','style':'width:221px','placeholder':'Seleccione ...'}))
    Fecha   = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(attrs={'tabindex':'2','class':'input-xlarge','placeholder':'Fecha reserva...','style':'width:198px', 'readonly':'readonly'}), error_messages={'required': 'Obligatorio'})
    ##Hora    = forms.CharField(initial='00:00', widget=forms.Select(choices=HORA_CHOICES, attrs={'tabindex':'3','style':'width:100px'}))
    Categoria = forms.ModelChoiceField(required=False, queryset=Category.objects.all().filter(status=True, type=1), empty_label=u'Todos', label=u'Categoría', widget=forms.Select(attrs={'tabindex':'5','style':'width:235px'}))

    #Categoria = forms.IntegerField(widget=forms.Select(choices=Category.objects.all().filter(status=True, type=1).values_list('id_category','title'), attrs={'tabindex':'4','style':'width:125px'}))

    ##Personas = forms.CharField(initial=1, widget=forms.Select(choices=PERSONAS_CHOICES, attrs={'tabindex':'5','style':'width:100px'}))

    #Estado = forms.IntegerField(widget=forms.Select(choices=TODOS_CHOICES, attrs={'tabindex':'6','style':'width:285px'}))
    #Estado = forms.ModelChoiceField(queryset = State.objects.all())

    Estado = forms.ModelChoiceField(initial=1, queryset=State.objects.all(), empty_label=u'Estado', error_messages={'required':'Obligatorio'}, label=u'Estado.', widget=forms.Select(attrs={'tabindex':'6','style':'width:235px'}))

    '''
    def __init__(self, *args, **kwargs):
        country_id = kwargs.pop('country_id', None)
        super(RestaurantForm, self).__init__(*args, **kwargs)

        if country_id:
            self.fields['Estado'].queryset = State.objects.all().filter(country_id=country_id)
    '''

type_choices = ( 
    (0, 'Reservar Mesa'),
    (1, 'Servicio a Domicilio'),
) 

class ReserveForm(forms.ModelForm):
    type        = forms.IntegerField(widget=forms.RadioSelect(choices=type_choices), error_messages={'required': 'Seleccione reserva o pedido'})
    name        = forms.CharField(widget=forms.TextInput(attrs={'class':'span2', 'tabindex':'1','placeholder':u'Nombre (*)'}), error_messages={'required': '* Nombre: Obligatorio'})
    email       = forms.EmailField(widget=forms.TextInput(attrs={'class':'span2', 'tabindex':'2','placeholder':u'Email (*)'}), error_messages={'required': '* Email: Obligatorio', 'invalid': '* Inserte un Email no válido' })
    address     = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'span2', 'tabindex':'3','placeholder':u'Dirección'}))
    phone       = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'span2', 'tabindex':'3','placeholder':u'Teléfono'}))
    people      = forms.CharField(initial=1, widget=forms.Select(choices=PERSONAS_CHOICES, attrs={'class':'span2', 'tabindex':'4'}), error_messages={'required': '* Personas: Obligatorio'})
    date        = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(attrs={'tabindex':'5','class':'span2','placeholder':'Fecha', 'readonly':'readonly'}), error_messages={'required': '* Fecha: Obligatorio'})
    time        = forms.CharField(initial='00:00', widget=forms.Select(choices=HORA_CHOICES, attrs={'tabindex':'6','class':'span2'}), error_messages={'required': '* Hora: Obligatorio'})
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':'3','class':'span2','placeholder':'Descripción o detalles de su reserva.'}))
    # initial=datetime.date.today,
    class Meta:
        model = Reserve
        exclude = {'status', 'user', 'directory', 'date_create', 'date_update'}

class CommentForm(forms.ModelForm):
    name        = forms.CharField(required=False, widget=forms.TextInput(attrs={'tabindex':'1','placeholder':u'Inserte su Nombre'}))
    email       = forms.EmailField(widget=forms.TextInput(attrs={'tabindex':'2','placeholder':u'Inserte su Email'}), error_messages={'required': 'Campo obligatorio', 'invalid': 'Inserte un Email no válido' })
    comment     = forms.CharField(widget=forms.Textarea(attrs={'rows':'7','tabindex':'3','placeholder':'Inserte un comentario.'}), error_messages={'required': 'Campo obligatorio'})

    class Meta:
        model = Comment
        exclude = {'status', 'directory', 'user', 'date_create'}

class RateForm(forms.ModelForm):

    class Meta:
        model = Rate
        exclude = {'directory', 'value', 'date_create'}

