from django.conf.urls import patterns, include, url

urlpatterns = patterns('zonetable.apps.search.views',
	url(r'^search/(?P<page>.*)/$','search_rest_view',name='go_search_rest'),
#	url(r'^search/$', 'search_rest_view', name='go_search_rest'),
)
