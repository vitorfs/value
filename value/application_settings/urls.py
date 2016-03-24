# coding: utf-8

from django.conf.urls import url

from value.application_settings import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admins/$', views.admins, name='admins'),
    url(r'^items/$', views.items, name='items'),
    url(r'^items/save-ordering/$', views.save_ordering, name='save_ordering'),
    url(r'^items/save-import-templates/$', views.save_import_templates, name='save_import_templates'),
    url(r'^items/save-custom-fields/$', views.save_custom_fields, name='save_custom_fields'),
    url(r'^import/$', views.import_template, name='import'),
]
