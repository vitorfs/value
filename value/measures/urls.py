from django.conf.urls import patterns, include, url

urlpatterns = patterns('value.measures.views',
    url(r'^$', 'measures', name='measures'),
    url(r'^add/$', 'add', name='add'),
    url(r'^(\d+)/$', 'measure', name='measure'),
    url(r'^(\d+)/delete/$', 'delete', name='delete'),
)
