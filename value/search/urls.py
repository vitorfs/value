from django.conf.urls import patterns, include, url

urlpatterns = patterns('value.search.views',
    url(r'^$', 'index', name='index'),
)
