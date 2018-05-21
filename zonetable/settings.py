# Django settings for zonetable project.
import os
DEBUG = True
TEMPLATE_DEBUG = DEBUG
#PREPEND_WWW = True

ADMINS = (
    ('ZoneTable', 'info@f.com'),
)

URL_SITE = 'http://www.f.com/'

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['localhost', ]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-ES'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__),'static/'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

STATIC_ROOT = ''

# URL prefix for static files.
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(MEDIA_ROOT),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'zonetable.urls'

#Identificar o definir el perfil de los usuarios
AUTH_PROFILE_MODULE = 'accounts.UserProfile'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'zonetable.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__),'templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    #
    'zonetable.apps.accounts',
    #'zonetable.apps.accounts.payments',
    'zonetable.apps.accounts.sheets',
    'zonetable.apps.home',
    'zonetable.apps.directory',
    'zonetable.apps.search',
    'zonetable.apps.multiuploader',
    'zonetable.apps.sorl.thumbnail',
    #
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'south',
    #'tinymce',
    'storages',
    'gunicorn',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    #'django.contrib.messages.context_processors.messages',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Configuracion del correo

EMAIL_FROM = 'info@f.com'
EMAIL_TO = 'info@f.com'

# MULTIUPLOAD
MULTI_FILE_DELETE_URL = 'multi_delete'
MULTI_IMAGE_URL = 'multi_image'
MULTI_IMAGES_FOLDER = 'multiuploader_images'

#TINYMCE
'''
TINYMCE_JS_URL = '/static/js/tiny_mce/tiny_mce_src.js'
URL_FILEBROWSER_MEDIA = '/static/js/filebrowser/'
FILEBROWSER_URL_TINYMCE = '/static/js/tiny_mce/'
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,spellchecker,paste,searchreplace",
    'theme': "advanced",
    'theme_advanced_toolbar_location':"top",
    'cleanup_on_startup': True,
}

TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = True
'''

TINYMCE_JS_URL = '/static/js/tiny_mce/tiny_mce.js'
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,paste,searchreplace,advimage,advlink,fullpage,fullscreen,visualchars,preview,media,insertdatatime,directionality,contextmenu,wordc",
    'theme_advanced_path_location' : "bottom",
    'theme_advanced_buttons1' : "fullscreen,separator,preview,separator,media,cut,copy,paste,separator,undo,redo,separator,search,replace,separator,code,separator,cleanup,separator,bold,italic,underline,strikethrough,separator,forecolor,backcolor,separator,justifyleft,justifycenter,justifyright,justifyfull,separator,help",
    'theme_advanced_buttons2' : "removeformat,styleselect,formatselect,fontselect,fontsizeselect,separator,bullist,numlist,outdent,indent,separator,link,unlink,anchor",
    'theme_advanced_buttons3' : "sub,sup,separator,image,insertdate,inserttime,separator,tablecontrols,separator,hr,advhr,visualaid,separator,charmap,emotions,iespell,flash,separator,print",
    'mode': 'textareas',
    'theme': 'advanced',
    'theme_advanced_toolbar_location': 'top',
    'advimage_update_dimensions_onchange': True,
    'browsers': 'gecko',
    'dialog_type': 'modal',
    'object_resizing': True,
    'cleanup_on_startup': True,
    'forced_root_block': 'p',
    'remove_trailing_nbsp': True,
    'height': '350',
}

FILEBROWSER_MEDIA_URL = '/static/js/'
FILEBROWSER_URL_FILEBROWSER_MEDIA = '/static/js/filebrowser/'
FILEBROWSER_URL_TINYMCE = "/static/js/tiny_mce/"
FILEBROWSER_PATH_TINYMCE = "js/tiny_mce/"

PAYPAL_EMAIL = ''
PAYPAL_RETURN_URL = URL_SITE + 'accounts/payments/'

# live
PAYPAL_URL = 'https://www.paypal.com/'
PAYPAL_PDT_URL = 'https://www.paypal.com/'


# Storage S3

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

MEDIA_ROOT = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2] + ['media'])
STATIC_ROOT = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2] + ['content'])

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_STORAGE_BUCKET_NAME = ''
