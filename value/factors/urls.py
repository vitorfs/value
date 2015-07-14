from django.conf.urls import patterns, include, url

urlpatterns = patterns('value.factors.views',
    url(r'^$', 'factors', name='factors'),
    url(r'^add/$', 'add', name='add'),
    url(r'^(\d+)/$', 'factor', name='factor'),
    url(r'^(\d+)/delete/$', 'delete', name='delete'),
    url(r'^groups/$', 'groups', name='groups'),
    url(r'^groups/add/$', 'add_group', name='add_group'),
)
