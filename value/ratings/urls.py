from django.conf.urls import patterns, include, url

urlpatterns = patterns('value.ratings.views',
    url(r'^$', 'ratings', name='ratings'),
    url(r'^add/$', 'add_rating', name='add_rating'),
    url(r'^(\d+)/$', 'rating', name='rating'),
)
