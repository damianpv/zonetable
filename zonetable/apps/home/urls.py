from django.conf.urls import patterns, include, url

urlpatterns = patterns('zonetable.apps.home.views',
	url(r'^$','home_view',name='go_principal'),
	
	#url(r'^loginfb/$','home_fb_view',name='go_home_original'),
	#url(r'^orig/$','home_original_view',name='go_home_original'),

	url(r'^contact/$','contact_view',name='go_contact'),
	url(r'^test_ip/$','test_ip',name='test_ip'),
	
	
	url(r'^faq/$','faq_view',name='go_faq'),
	url(r'^affiliate/$','affiliate_view',name='go_affiliate'),

	#url(r'^terminos-condiciones/$','terms_view',name='vista_terminos'),
	#url(r'^politicas-privacidad/$','privacy_view',name='vista_privacidad'),
	#url(r'^faq/$','faq_view',name='vista_faq'),

	url(r'^(privacy-policy)/$','content_view',name='go_privacy'),
	url(r'^(terms-conditions)/$','content_view',name='go_terms'),

	#url(r'(test1)/$','content_view',name='vista_contenidos'),
	#url(r'^contenidos/(?P<id_prod>.*)/$','content_view',name='vista_contenidos'),

	#url(r'^about/$','about_view',name='vista_about'),
	#url(r'^productos/page/(?P<pagina>.*)/$','productos_view',name='vista_productos'),
	#url(r'^producto/(?P<id_prod>.*)/$','singleProduct_view',name='vista_single_producto'),
	#url(r'^login/$','login_view',name='vista_login'),
	#url(r'^logout/$','logout_view',name='vista_logout'),
)
