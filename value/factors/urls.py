from django.conf.urls import patterns, include, url

urlpatterns = patterns('value.factors.views',
    url(r'^$', 'factors', name='factors'),
    url(r'^add/$', 'add', name='add'),
    url(r'^(\d+)/$', 'factor', name='factor'),
    url(r'^(\d+)/delete/$', 'delete', name='delete'),
    url(r'^groups/$', 'groups', name='groups'),
    url(r'^groups/add/$', 'add_group', name='add_group'),
    url(r'^groups/add-factor/$', 'add_factor_group', name='add_factor_group'),
    url(r'^groups/delete/$', 'delete_group', name='delete_group'),
)
