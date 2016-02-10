# coding: utf-8

from django.conf.urls import patterns, include, url

from value.measures import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.add, name='add'),
    url(r'^(\d+)/$', views.edit, name='edit'),
    url(r'^(\d+)/delete/$', views.delete, name='delete'),
    url(r'^active/$', views.toggle_active, name='toggle_active'),
]
