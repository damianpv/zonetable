from django.conf.urls import patterns, include, url

urlpatterns = patterns('zonetable.apps.testing.views',
    url(r'^test/$','testing_view',name='go_testing'),
)
