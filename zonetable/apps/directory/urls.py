from django.conf.urls import patterns, include, url

urlpatterns = patterns('zonetable.apps.directory.views',
    url(r'^set_rate/$', 'set_rate_view',name='go_set_rate'), 
	url(r'^dir_test/$', 'directory_test_view', name='go_test_directory'),
    url(r'^get_restaurant/$', 'get_rest_view',name='go_get_restaurant'), 
	url(r'^category/$', 'category_view', name='go_category'),
	#url(r'^category/(?P<url_name>.*)/$', 'directory_category_view', name='go_directory_category'),
	#url(r'^category/(?P<url_name>.*)/(?P<page>.*)/$','directory_category_paginar_view',name='go_directory_category'),
	#url(r'^category/(?P<url_name>.*)/$','directory_category_paginar_view',name='go_directory_category'),
	url(r'^category/(?P<url_name>.*)/(?P<page>.*)/$','directory_category_view',name='go_directory_category'),
	#url(r'^category/(?P<url_name>.*)/$','directory_category_view',name='go_directory_category'),

	url(r'^(?P<url_name>.*)/$', 'directory_view', name='go_directory'),
)
