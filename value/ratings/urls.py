from django.conf.urls import patterns, include, url

urlpatterns = patterns('value.ratings.views',
    url(r'^$', 'ratings', name='ratings'),
)
