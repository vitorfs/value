from django.conf.urls import patterns, include, url

urlpatterns = patterns('value.help.views',
    url(r'^$', 'index', name='index'),
)
