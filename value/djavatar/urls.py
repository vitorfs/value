from django.conf.urls import patterns, include, url

urlpatterns = patterns('value.djavatar.views',
    url(r'^(?P<initials>[^/]+)$', 'avatar', name='avatar'),
)
