from django.conf.urls import patterns, include, url

urlpatterns = patterns('value.factors.views',
    url(r'^$', 'index', name='index'),
    url(r'^add/$', 'add', name='add'),
    url(r'^(\d+)/$', 'edit', name='edit'),
    url(r'^(\d+)/delete/$', 'delete', name='delete'),
    url(r'^active/$', 'toggle_active', name='toggle_active'),
    url(r'^groups/$', 'groups', name='groups'),
    url(r'^groups/add/$', 'add_group', name='add_group'),
    url(r'^groups/(\d+)/$', 'edit_group', name='edit_group'),
    url(r'^groups/delete/$', 'delete_group', name='delete_group'),
    url(r'^groups/add-factor/$', 'add_factor_group', name='add_factor_group'),
)
