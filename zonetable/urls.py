from django.http import HttpResponse

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
import settings

from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = staticfiles_urlpatterns()
urlpatterns += patterns('',

    url(r'^admin/', include(admin.site.urls)),

    #url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),

    url(r'^robots\.txt$', TemplateView.as_view(template_name='seo/robots.txt'), name="robots"),
    url(r'^sitemap\.xml$', TemplateView.as_view(template_name='seo/sitemap.xml'), name="sitemap"),
    url(r'^google\.html$', TemplateView.as_view(template_name='seo/k.html'), name="google"),

    #url(r'', include('zonetable.apps.filebrowser.urls')),
    url(r'', include('zonetable.apps.multiuploader.urls')),
    url(r'', include('zonetable.apps.accounts.urls')),
    #url(r'', include('zonetable.apps.accounts.payments.urls')),
    url(r'', include('zonetable.apps.accounts.sheets.urls')),
    url(r'', include('zonetable.apps.accounts.reservation.urls')),
    url(r'', include('zonetable.apps.home.urls')),
    url(r'', include('zonetable.apps.functions.urls')),
    url(r'', include('zonetable.apps.search.urls')),
    url(r'', include('zonetable.apps.testing.urls')),

    url(r'', include('zonetable.apps.directory.urls')),

    #url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
