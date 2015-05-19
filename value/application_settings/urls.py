from django.conf.urls import patterns, include, url

urlpatterns = patterns('value.application_settings.views',
    url(r'^$', 'index', name='index'),
)
