# coding: utf-8

from django.conf.urls import url

from value.factors import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.add, name='add'),
    url(r'^(\d+)/$', views.edit, name='edit'),
    url(r'^(\d+)/delete/$', views.delete, name='delete'),
    url(r'^active/$', views.toggle_active, name='toggle_active'),
    url(r'^groups/$', views.groups, name='groups'),
    url(r'^groups/add/$', views.add_group, name='add_group'),
    url(r'^groups/(\d+)/$', views.edit_group, name='edit_group'),
    url(r'^groups/delete/$', views.delete_group, name='delete_group'),
    url(r'^groups/add-factor/$', views.add_factor_group, name='add_factor_group'),
]
