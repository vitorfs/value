from django.conf.urls import patterns, include, url

urlpatterns = patterns('value.deliverables.meetings.views',
    url(r'^$', 'index', name='index'),
    url(r'^new/$', 'new', name='new'),
    url(r'^(?P<meeting_id>\d+)/$', 'meeting', name='meeting'),
    url(r'^(?P<meeting_id>\d+)/close/$', 'close_meeting', name='close_meeting'),
    url(r'^(?P<meeting_id>\d+)/open/$', 'open_meeting', name='open_meeting'),
    url(r'^(?P<meeting_id>\d+)/remove-stakeholder/$', 'remove_stakeholder', name='remove_stakeholder'),
    url(r'^(?P<meeting_id>\d+)/evaluate/$', 'evaluate', name='evaluate'),
    url(r'^(?P<meeting_id>\d+)/evaluate/save/$', 'save_evaluation', name='save_evaluation'),
    url(r'^(?P<meeting_id>\d+)/evaluate/rationale/save/$', 'save_rationale', name='save_rationale'),

    url(r'^(?P<meeting_id>\d+)/dashboard/$', 'dashboard', name='dashboard'),
    url(r'^(?P<meeting_id>\d+)/dashboard/download/$', 'download', name='download'),
    url(r'^(?P<meeting_id>\d+)/dashboard/factors-usage/$', 'dashboard_factors_usage_chart', name='dashboard_factors_usage_chart'),
    url(r'^(?P<meeting_id>\d+)/dashboard/stakeholders-input/$', 'dashboard_stakeholders_input_chart', name='dashboard_stakeholders_input_chart'),

    url(r'^(?P<meeting_id>\d+)/dashboard/features/$', 'features', name='features'),
    url(r'^(?P<meeting_id>\d+)/dashboard/features/(?P<meeting_item_id>\d+)/$', 'features_chart', name='features_chart'),

    url(r'^(?P<meeting_id>\d+)/dashboard/features-acceptance/$', 'features_acceptance', name='features_acceptance'),
    url(r'^(?P<meeting_id>\d+)/dashboard/features-acceptance/(?P<meeting_item_id>\d+)/$', 'features_acceptance_chart', name='features_acceptance_chart'),

    url(r'^(?P<meeting_id>\d+)/dashboard/decision-items-overview/$', 'decision_items_overview', name='decision_items_overview'),

    url(r'^(?P<meeting_id>\d+)/dashboard/features-comparison/$', 'features_comparison', name='features_comparison'),
    url(r'^(?P<meeting_id>\d+)/dashboard/features-comparison/(?P<measure_value_id>\d+)/$', 'features_comparison_chart', name='features_comparison_chart'),

    url(r'^(?P<meeting_id>\d+)/settings/$', 'settings', name='settings'),
    url(r'^(?P<meeting_id>\d+)/delete/$', 'delete', name='delete'),
)
