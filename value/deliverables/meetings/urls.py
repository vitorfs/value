from django.conf.urls import patterns, include, url

urlpatterns = patterns('value.deliverables.meetings.views',
    url(r'^$', 'index', name='index'),
    url(r'^new/$', 'new', name='new'),
    url(r'^(?P<meeting_id>\d+)/$', 'meeting', name='meeting'),
    url(r'^(?P<meeting_id>\d+)/stakeholders/$', 'stakeholders', name='stakeholders'),
    url(r'^(?P<meeting_id>\d+)/meeting-items/$', 'meeting_items', name='meeting_items'),
    url(r'^(?P<meeting_id>\d+)/evaluate/$', 'evaluate', name='evaluate'),
    url(r'^(?P<meeting_id>\d+)/evaluate/save/$', 'save_evaluation', name='save_evaluation'),
    url(r'^(?P<meeting_id>\d+)/dashboard/$', 'dashboard', name='dashboard'),
    url(r'^(?P<meeting_id>\d+)/dashboard/features/$', 'features', name='features'),
    url(r'^(?P<meeting_id>\d+)/dashboard/features/(?P<item_id>\d+)/$', 'features_chart', name='features_chart'),
    url(r'^(?P<meeting_id>\d+)/dashboard/features-acceptance/$', 'features_acceptance', name='features_acceptance'),
    url(r'^(?P<meeting_id>\d+)/dashboard/features-acceptance/(?P<item_id>\d+)/$', 'features_acceptance_chart', name='features_acceptance_chart'),
    url(r'^(?P<meeting_id>\d+)/dashboard/features-comparison/$', 'features_comparison', name='features_comparison'),
)
