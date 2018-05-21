# -*- coding: utf-8 -*-

from django import forms

COMO_CONOCIO_CHOICES = (
    ('0', 'Seleccione'),
    ('1', 'Buscador'),
    ('2', 'Un amigo'),
    ('3', 'Publicidad'),
    ('4', 'Otro sitio web'),
)

STATUS_CHOICES = (
    ('', 'Seleccione'),
    ('1', 'Duda y/o sugerencia'),
    ('2', 'Comentario'),
)

class ContactForm(forms.Form):
    Nombre  = forms.CharField(widget=forms.TextInput(attrs={'class':'input-xlarge','placeholder':'Inserte su Nombre...'}), error_messages={'required': 'Campo obligatorio'})
    Email   = forms.EmailField(widget=forms.TextInput(attrs={'class':'input-xlarge','placeholder':'Inserte su Email...'}), error_messages={'required': 'Campo obligatorio'})
    Telefono    = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'input-xlarge','placeholder':u'Inserte su Teléfono...'}))
    Como_conocio = forms.CharField(required=False,widget=forms.Select(choices=COMO_CONOCIO_CHOICES))
    Asunto = forms.CharField(widget=forms.Select(choices=STATUS_CHOICES), error_messages={'required': 'Campo obligatorio'})
    Comentarios = forms.CharField(widget=forms.Textarea(attrs={'rows':'8','class':'input-xxlarge','placeholder':'Inserte su Comentario...'}), error_messages={'required': 'Campo obligatorio'})
