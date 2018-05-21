# -*- coding: utf-8 -*-
from django.contrib import admin
from zonetable.apps.directory.models import Category, Service, Payment, Currency, Style, Comment, Directory, Reserve, Package, Pay

class ContactOptions(admin.ModelAdmin):
    class Media:
        #ruta al javascript de TinyMCE y de textarea.js 
        #importante poner ../ en la ruta. Esto puede cambiar según tu urls.py
        js = ('js/tiny_mce/tiny_mce.js', 
              'js/tiny_mce/textareas.js')

admin.site.register(Category)
admin.site.register(Service)
admin.site.register(Payment)
admin.site.register(Currency)
admin.site.register(Style)
admin.site.register(Comment)
admin.site.register(Pay)
admin.site.register(Directory, ContactOptions)
admin.site.register(Reserve, ContactOptions)
admin.site.register(Package, ContactOptions)
