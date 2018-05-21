from django.conf.urls import patterns, include, url

urlpatterns = patterns('zonetable.apps.accounts.reservation.views',
    url(r'^accounts/reservation/(?P<id_sheets>.*)/add/$', 'add_reservation_view',name='go_add_reservation'),
    url(r'^accounts/reservation/(?P<id_sheets>.*)/(?P<id_reservation>.*)/edit/$', 'edit_reservation_view',name='go_edit_reservation'),
    url(r'^accounts/reservation/(?P<id_sheets>\d+)/(?P<id_reservation>\d+)/(?P<url_name>.*)/$', 'set_status_reservation_view',name='set_status_reservation'),
    url(r'^accounts/reservation/(?P<id_sheets>.*)/(?P<id_page>.*)/$', 'list_reservation_view',name='go_list_reservation'),
    url(r'^accounts/reservation/set_complete/(?P<id_page>.*)/$', 'list_reservation_view',name='go_list_reservation'),
)