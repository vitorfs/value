from django.conf.urls import patterns, include, url

urlpatterns = patterns('value.users.views',
    url(r'^$', 'users', name='users'),
    url(r'^add/$', 'add', name='add'),
    url(r'^(?P<username>[^/]+)/$', 'user', name='user'),
    url(r'^(?P<username>[^/]+)/password/$', 'password', name='password'),
    url(r'^(?P<username>[^/]+)/delete/$', 'delete', name='delete'),
)
