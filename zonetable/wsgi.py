import os, sys
sys.path.append('/proj/public_html/zonetable')
os.environ['DJANGO_SETTINGS_MODULE'] = 'zonetable.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
