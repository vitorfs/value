from django.conf.urls import patterns, include, url

urlpatterns = patterns('value.workspace.analyze.views',
    url(r'^$', 'index', name='index'),

    url(r'^features/$', 'features', name='features'),
    url(r'^features/(?P<item_id>\d+)/$', 'features_chart', name='features_chart'),

    url(r'^features-acceptance/$', 'features_acceptance', name='features_acceptance'),
    url(r'^features-acceptance/(?P<item_id>\d+)/$', 'features_acceptance_chart', name='features_acceptance_chart'),
    
    url(r'^features-acceptance-factors/$', 'features_acceptance_factors', name='features_acceptance_factors'),
    url(r'^features-drilldown/$', 'features_drilldown', name='features_drilldown'),
)
