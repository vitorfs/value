# coding: utf-8

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^summary/$', views.value_summary, name='value_summary'),
    url(r'^charts/$', views.charts, name='charts'),
]
