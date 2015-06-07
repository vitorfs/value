from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static


urlpatterns = patterns('',
    url(r'^$', 'value.core.views.home', name='home'),
    url(r'^signin/$', 'django.contrib.auth.views.login', name='signin'),
    url(r'^signout/$', 'django.contrib.auth.views.logout', { 'next_page': '/' }, name='signout'),
    url(r'^reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^reset/sent/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),
    url(r'^account/$', 'value.users.views.account', name='account'),
    url(r'^account/password/$', 'value.users.views.change_password', name='change_password'),
    url(r'^settings/', include('value.application_settings.urls', namespace='settings')),
    url(r'^factors/', include('value.factors.urls', namespace='factors')),
    url(r'^groups/', include('value.groups.urls', namespace='groups')),
    url(r'^measures/', include('value.measures.urls', namespace='measures')),
    url(r'^search/', include('value.search.urls', namespace='search')),
    url(r'^users/', include('value.users.urls', namespace='users')),
    url(r'^help/', include('value.help.urls', namespace='help')),
    url(r'^deliverables/', include('value.deliverables.urls', namespace='deliverables')),
    url(r'^avatar/', include('value.avatar.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    