from django.conf.urls import patterns, include, url

urlpatterns = patterns('zonetable.apps.accounts.payments.views',
    url(r'^accounts/payments/$', 'ok_payments_view',name='go_ok_payments'),
    url(r'^accounts/payments/(?P<id_payment>.*)/cancel/$', 'cancel_payments_view',name='go_cancel_payments'),
    url(r'^accounts/payments/cancel/$', 'redirect_cancel_payments_view',name='go_redirect_cancel_payments'),
    url(r'^accounts/payments/history/(?P<page>.*)/$', 'list_payments_view',name='go_list_payments'),
)
