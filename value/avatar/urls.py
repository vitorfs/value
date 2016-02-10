# coding: utf-8

from django.conf.urls import patterns, include, url

from value.avatar import views


urlpatterns = [
    url(r'^(?P<initials>[^/]+)$', views.avatar, name='avatar'),
]
