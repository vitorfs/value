from django.conf.urls import patterns, include, url

urlpatterns = patterns('value.workspace.views',
    url(r'^$', 'index', name='index'),
    url(r'^(\d+)/$', 'instance', name='instance'),
)
