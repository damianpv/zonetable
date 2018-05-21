# -*- coding: utf-8 -*-
from django.contrib import admin
from zonetable.apps.home.models import City, State, Country, Contact, Content

#info encontrada en: http://code.djangoproject.com/wiki/AddWYSIWYGEditor
class ContactOptions(admin.ModelAdmin):
    class Media:
        #ruta al javascript de TinyMCE y de textarea.js 
        #importante poner ../ en la ruta. Esto puede cambiar según tu urls.py
        js = ('js/tiny_mce/tiny_mce.js', 
              'js/tiny_mce/textareas.js',
              'filebrowser/js/TinyMCEAdmin.js',)

admin.site.register(Contact, ContactOptions)
admin.site.register(Content)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
