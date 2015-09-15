# coding: utf-8

from django.conf.urls import patterns, include, url


urlpatterns = patterns('value.users.views',
    url(r'^$', 'users', name='users'),
    url(r'^add/$', 'add', name='add'),
    url(r'^(\d+)/$', 'user', name='user'),
    url(r'^(\d+)/password/$', 'password', name='password'),
    url(r'^(\d+)/delete/$', 'delete', name='delete'),
    url(r'^active/$', 'toggle_active', name='toggle_active'),
    url(r'^roles/$', 'roles', name='roles'),
    url(r'^roles/add/$', 'add_role', name='add_role'),
    url(r'^roles/(\d+)/$', 'edit_role', name='edit_role'),
    url(r'^roles/delete/$', 'delete_role', name='delete_role'),
    url(r'^roles/add-user/$', 'add_user_role', name='add_user_role'),
    url(r'^roles/remove-user/$', 'remove_user_role', name='remove_user_role'),
)
