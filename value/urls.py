from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'value.core.views.home', name='home'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'core/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^models/', include('value.models.urls', namespace='models')),
    url(r'^factors/', include('value.factors.urls', namespace='factors')),
    url(r'^ratings/', include('value.ratings.urls', namespace='ratings')),
    url(r'^users/', include('value.users.urls', namespace='users')),
    url(r'^help/', include('value.help.urls', namespace='help')),
)
