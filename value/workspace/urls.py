from django.conf.urls import patterns, include, url

urlpatterns = patterns('value.workspace.views',
    url(r'^$', 'index', name='index'),
    url(r'^new/$', 'new', name='new'),
    url(r'^(\d+)/$', 'instance', name='instance'),
    url(r'^(\d+)/evaluate/$', 'evaluate', name='evaluate'),
)
