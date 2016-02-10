# coding: utf-8

from django.conf.urls import patterns, include, url

from value.help import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
