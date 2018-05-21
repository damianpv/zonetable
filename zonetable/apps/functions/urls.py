from django.conf.urls import patterns, include, url

urlpatterns = patterns('zonetable.apps.functions.views',
	url(r'^whois_set/ajax/$','whois_set_view',name='go_set_whois'),
	url(r'^whois_get/ajax/$','whois_get_view',name='go_get_whois'),
)
