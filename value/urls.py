from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^$', 'value.core.views.home', name='home'),
    url(r'^signin/$', 'django.contrib.auth.views.login', { 'template_name' : 'core/signin.html' }, name='signin'),
    url(r'^signout/$', 'django.contrib.auth.views.logout', { 'next_page' : '/' }, name='signout'),
    url(r'^account/$', 'value.users.views.account', name='account'),
    url(r'^account/password/$', 'value.users.views.change_password', name='change_password'),
    url(r'^settings/', include('value.application_settings.urls', namespace='settings')),
    url(r'^factors/', include('value.factors.urls', namespace='factors')),
    url(r'^measures/', include('value.measures.urls', namespace='measures')),
    url(r'^search/', include('value.search.urls', namespace='search')),
    url(r'^users/', include('value.users.urls', namespace='users')),
    url(r'^help/', include('value.help.urls', namespace='help')),
    url(r'^deliverables/', include('value.deliverables.urls', namespace='deliverables')),
    url(r'^avatar/', include('value.avatar.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    