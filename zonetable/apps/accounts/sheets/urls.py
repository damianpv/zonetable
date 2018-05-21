from django.conf.urls import patterns, include, url

urlpatterns = patterns('zonetable.apps.accounts.sheets.views',
    url(r'^accounts/package/$', 'list_package_view',name='go_list_package'),
    url(r'^accounts/sheets/package/$', 'list_package_view',name='go_list_package'),
    url(r'^accounts/sheets/delete/(?P<id_directory>.*)/$', 'delete_sheets_view',name='go_delete_sheets'),
    url(r'^accounts/sheets/deactivate/(?P<id_directory>.*)/$', 'deactivate_sheets_view',name='go_deactivate_sheets'),
    url(r'^accounts/sheets/activate/(?P<id_directory>.*)/$', 'activate_sheets_view',name='go_activate_sheets'),
    url(r'^accounts/sheets/edit/(?P<id_directory>.*)/$', 'edit_sheets_view',name='go_edit_sheets'),
    url(r'^accounts/sheets/gallery/(?P<id_directory>.*)/$', 'gallery_sheets_view',name='go_gallery_sheets'),
    url(r'^accounts/sheets/add/$', 'add_sheets_view',name='go_add_sheets'),
    url(r'^accounts/sheets/(?P<page>.*)/$', 'list_sheets_view',name='go_list_sheets'),
)
