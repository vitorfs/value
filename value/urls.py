from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'value.core.views.home', name='home'),
)
