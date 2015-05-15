from django.conf.urls import patterns, include, url

urlpatterns = patterns('value.avatar.views',
    url(r'^(?P<initials>[^/]+)$', 'avatar', name='avatar'),
)
