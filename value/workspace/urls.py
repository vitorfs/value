from django.conf.urls import patterns, include, url

urlpatterns = patterns('value.workspace.views',
    url(r'^$', 'index', name='index'),
    url(r'^new/$', 'new', name='new'),
    url(r'^(\d+)/$', 'instance', name='instance'),
    url(r'^(\d+)/evaluate/$', 'evaluate', name='evaluate'),
    url(r'^(\d+)/evaluate/save/$', 'save_evaluation', name='save_evaluation'),
    url(r'^(\d+)/stakeholders/$', 'stakeholders', name='stakeholders'),
    url(r'^(\d+)/analyze/$', 'analyze', name='analyze'),
    url(r'^(\d+)/analyze/features/$', 'analyze_features', name='analyze_features'),
    url(r'^(\d+)/analyze/features-acceptance/$', 'analyze_features_acceptance', name='analyze_features_acceptance'),
    url(r'^(\d+)/analyze/features-acceptance-factors/$', 'analyze_features_acceptance_factors', name='analyze_features_acceptance_factors'),
    url(r'^(\d+)/analyze/features-drilldown/$', 'analyze_features_drilldown', name='analyze_features_drilldown'),
)
