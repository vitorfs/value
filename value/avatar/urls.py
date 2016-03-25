# coding: utf-8

from django.conf.urls import url

from value.avatar import views


urlpatterns = [
    url(r'^(?P<initials>[^/]+)$', views.avatar, name='avatar'),
]
