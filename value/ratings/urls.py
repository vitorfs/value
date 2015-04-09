from django.conf.urls import patterns, include, url

urlpatterns = patterns('value.ratings.views',
    url(r'^$', 'ratings', name='ratings'),
    url(r'^add/$', 'add', name='add'),
    url(r'^(\d+)/$', 'rating', name='rating'),
    url(r'^(\d+)/delete/$', 'delete', name='delete'),
)
