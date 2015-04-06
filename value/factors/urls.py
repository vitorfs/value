from django.conf.urls import patterns, include, url

urlpatterns = patterns('value.factors.views',
    url(r'^$', 'factors', name='factors'),
)
