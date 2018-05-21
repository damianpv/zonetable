from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('multiuploader/multiuploader_main.html')
def multiupform(id_directory):
    return {
    			'STATIC_URL':settings.STATIC_URL,
    			'id_directory':id_directory
    		}