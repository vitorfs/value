# coding: utf-8

from django.conf.urls import patterns, include, url


urlpatterns = patterns('value.users.views',
    url(r'^$', 'users', name='users'),
    url(r'^add/$', 'add', name='add'),
    url(r'^(\d+)/$', 'user', name='user'),
    url(r'^(\d+)/password/$', 'password', name='password'),
    url(r'^(\d+)/delete/$', 'delete', name='delete'),
    url(r'^roles/$', 'roles', name='roles'),
    url(r'^roles/add/$', 'add_role', name='add_role'),
    url(r'^roles/add-user/$', 'add_user_role', name='add_user_role'),
    url(r'^roles/remove-user/$', 'remove_user_role', name='remove_user_role'),
    url(r'groups/', include('value.users.groups.urls', namespace='groups')),
)
