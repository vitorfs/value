# coding: utf-8

from django.conf.urls import patterns, include, url

from value.users import views


urlpatterns = [
    url(r'^$', views.users, name='users'),
    url(r'^add/$', views.add, name='add'),
    url(r'^(\d+)/$', views.user, name='user'),
    url(r'^(\d+)/password/$', views.password, name='password'),
    url(r'^(\d+)/delete/$', views.delete, name='delete'),
    url(r'^active/$', views.toggle_active, name='toggle_active'),
    url(r'^roles/$', views.roles, name='roles'),
    url(r'^roles/add/$', views.add_role, name='add_role'),
    url(r'^roles/(\d+)/$', views.edit_role, name='edit_role'),
    url(r'^roles/delete/$', views.delete_role, name='delete_role'),
    url(r'^roles/add-user/$', views.add_user_role, name='add_user_role'),
    url(r'^roles/remove-user/$', views.remove_user_role, name='remove_user_role'),
]
