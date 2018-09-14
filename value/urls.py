# coding: utf-8

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from value.core import views as core_views
from value.users import views as users_views


urlpatterns = [
    url(r'^$', core_views.home, name='home'),
    url(r'^signin/$', auth_views.login, name='signin'),
    url(r'^signout/$', auth_views.logout, {'next_page': '/'}, name='signout'),
    url(r'^reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^reset/sent/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^account/$', users_views.account, name='account'),
    url(r'^account/password/$', users_views.change_password, name='change_password'),
    url(r'^account/language/$', login_required(TemplateView.as_view(template_name='users/language.html')),
        name='language'),

    url(r'^api/', include('value.api.urls', namespace='api')),
    url(r'^settings/', include('value.application_settings.urls', namespace='settings')),
    url(r'^factors/', include('value.factors.urls', namespace='factors')),
    url(r'^measures/', include('value.measures.urls', namespace='measures')),
    url(r'^users/', include('value.users.urls', namespace='users')),
    url(r'^help/', include('value.help.urls', namespace='help')),
    url(r'^deliverables/', include('value.deliverables.urls', namespace='deliverables')),

    url(r'^survey/(?P<uuid>[^/]+)/$', core_views.survey, name='survey'),
    url(r'^thanks/$', core_views.thanks, name='thanks'),

    url(r'^i18n/', include('django.conf.urls.i18n')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
