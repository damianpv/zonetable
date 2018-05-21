# -*- coding: utf-8 -*-

from django import forms

from zonetable.apps.home.models import Language, Country

class WhoisForm(forms.Form):
	Language 	= forms.IntegerField(widget=forms.Select(choices=Language.objects.all().filter(status=True).values_list('id_language','language'), attrs={'tabindex':'4','style':'width:164px'}))
	#Country 	= forms.ModelChoiceField(queryset = Country.objects.all())	
	#Country		= forms.ModelChoiceField(queryset=Country.objects.all(), empty_label=u'Country', error_messages={'required':'Campo obligatorio'}, label=u'Country.', widget=forms.Select(attrs={'tabindex':'6','style':'width:164px'}))
	#Country 	= forms.IntegerField(widget=forms.Select(choices=Country.objects.all().values_list('id_country','country'), attrs={'tabindex':'4','style':'width:164px'}))
	#Country        = forms.ModelChoiceField(queryset = Country.objects.all())
	#Country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label=u'Country', error_messages={'required':'Campo obligatorio'}, label=u'Country.', widget=forms.Select(attrs={'tabindex':'6','style':'width:164px'}))

	#permite filtrar el pais de la cookie
	Country 	= forms.ModelChoiceField(queryset = Country.objects.all().filter(status=True), empty_label=u'--- Seleccione uno ---', error_messages={'required':'Campo obligatorio'}, label=u'Country.', widget=forms.Select(attrs={'tabindex':'6','style':'width:164px'}))
