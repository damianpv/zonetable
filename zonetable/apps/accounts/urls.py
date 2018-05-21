from django.conf.urls import patterns, include, url

urlpatterns = patterns('zonetable.apps.accounts.views',
    url(r'^accounts/login/ajax/$', 'login_view',name='go_login'),
    url(r'^accounts/forgot/ajax/$', 'forgot_view',name='go_forgot'),
    url(r'^accounts/user_redsocial/ajax/$', 'user_fb_view',name='go_user_fb'),
    url(r'^accounts/user_validate/ajax/$', 'user_validate_view',name='go_user_validate'),

    url(r'^accounts/dashboard/$', 'view_dashboard_view',name='go_dashboard'),
    url(r'^accounts/profile/$', 'edit_user_profile_view',name='go_user_profile'),
    url(r'^accounts/my-reservations/(?P<id_reservation>.*)/cancel/$', 'cancel_user_reservation_view',name='go_cancel_user_reservation'),
    url(r'^accounts/my-reservations/(?P<id_reservation>.*)/edit/$', 'edit_user_reservation',name='go_edit_user_reservation'),
    url(r'^accounts/my-reservations/(?P<page>.*)/$', 'list_user_reservation_view',name='go_list_user_reservation'),
    url(r'^accounts/referer/$', 'view_referer_view',name='go_referer'),

    url(r'^logout/$', 'logout_view',name='go_logout'),
    url(r'^get_state/$', 'get_state_view',name='go_get_state'),
    url(r'^register/$','register_view',name='go_register'),
    url(r'^referer/(?P<id_user>.*)/$','referer_view',name='go_referer'),
	url(r'^confirm/(?P<random>.*)/$', 'confirm_view', name='go_confirm'),

)
