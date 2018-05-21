import os
import sys

sys.path.append('/sites/zonetable/public_html')

os.environ['PYTHON_EGG_CACHE'] = '/sites/zonetable/public_html/.python-egg'

os.environ['DJANGO_SETTINGS_MODULE'] = 'zonetable.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
