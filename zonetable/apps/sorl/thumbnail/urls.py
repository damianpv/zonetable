from django.conf.urls import patterns, include, url
from zonetable.apps.sorl.thumbnail.conf import settings

if settings.THUMBNAIL_DUMMY:
    urlpatterns = patterns('',
        url('^thumbnail-dummy/(\d+)x(\d+)/$',
            'zonetable.apps.sorl.thumbnail.views.thumbnail_dummy',
            name='thumbnail_dummy',
        ),
    )
else:
    urlpatterns = patterns('',)
