from django.conf.urls import patterns, include, url

urlpatterns = patterns('value.models.views',
    url(r'^$', 'models', name='models'),
    url(r'^(\d+)/$', 'model', name='model'),
)
