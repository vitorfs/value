from django.conf.urls import patterns, include, url

urlpatterns = patterns('value.users.views',
    url(r'^$', 'users', name='users'),
)
