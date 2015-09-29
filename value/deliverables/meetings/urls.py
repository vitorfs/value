from django.conf.urls import patterns, include, url

urlpatterns = patterns('value.deliverables.meetings.views',
    url(r'^$', 'index', name='index'),
    url(r'^new/$', 'new', name='new'),
    url(r'^(?P<meeting_id>\d+)/$', 'meeting', name='meeting'),
    url(r'^(?P<meeting_id>\d+)/close/$', 'close_meeting', name='close_meeting'),
    url(r'^(?P<meeting_id>\d+)/open/$', 'open_meeting', name='open_meeting'),
    url(r'^(?P<meeting_id>\d+)/remove-stakeholder/$', 'remove_stakeholder', name='remove_stakeholder'),
    url(r'^(?P<meeting_id>\d+)/add-stakeholders/$', 'add_stakeholders', name='add_stakeholders'),
    url(r'^(?P<meeting_id>\d+)/remove-decision-items/$', 'remove_decision_items', name='remove_decision_items'),
    url(r'^(?P<meeting_id>\d+)/add-decision-items/$', 'add_decision_items', name='add_decision_items'),

    # Evaluate URLs
    url(r'^(?P<meeting_id>\d+)/evaluate/$', 'evaluate', name='evaluate'),
    url(r'^(?P<meeting_id>\d+)/evaluate/save/$', 'save_evaluation', name='save_evaluation'),
    url(r'^(?P<meeting_id>\d+)/evaluate/rationale/save/$', 'save_rationale', name='save_rationale'),

    # Dashboard URLs
    url(r'^(?P<meeting_id>\d+)/dashboard/$', 'dashboard', name='dashboard'),
    url(r'^(?P<meeting_id>\d+)/dashboard/download/$', 'download', name='download'),

    ## Summary Charts URLs
    url(r'^(?P<meeting_id>\d+)/dashboard/factors-usage/$', 'dashboard_factors_usage_chart', name='dashboard_factors_usage_chart'),
    url(r'^(?P<meeting_id>\d+)/dashboard/stakeholders-input/$', 'dashboard_stakeholders_input_chart', name='dashboard_stakeholders_input_chart'),
    url(r'^(?P<meeting_id>\d+)/dashboard/value-ranking/$', 'value_ranking', name='value_ranking'),
    url(r'^(?P<meeting_id>\d+)/dashboard/decision-items-overview/$', 'decision_items_overview', name='decision_items_overview'),
    url(r'^(?P<meeting_id>\d+)/dashboard/features-comparison/$', 'features_comparison', name='features_comparison'),
    url(r'^(?P<meeting_id>\d+)/dashboard/features-comparison/(?P<measure_value_id>\d+)/$', 'features_comparison_chart', name='features_comparison_chart'),

    ## Detailed Charts URLs
    ### Factors Comparison URLs
    url(r'^(?P<meeting_id>\d+)/dashboard/factors/$', 'features', name='features'),
    url(r'^(?P<meeting_id>\d+)/dashboard/factors/(?P<meeting_item_id>\d+)/$', 'features_chart', name='features_chart'),
    url(r'^(?P<meeting_id>\d+)/dashboard/factors/scenarios/$', 'features_scenarios', name='features_scenarios'),
    url(r'^(?P<meeting_id>\d+)/dashboard/factors/scenarios/(?P<scenario_id>\d+)/$', 'features_scenario_chart', name='features_scenario_chart'),

    ### Factors Groups Comparison URLs
    url(r'^(?P<meeting_id>\d+)/dashboard/groups/$', 'factors_groups', name='factors_groups'),
    url(r'^(?P<meeting_id>\d+)/dashboard/groups/(?P<meeting_item_id>\d+)/$', 'factors_groups_chart', name='factors_groups_chart'),
    url(r'^(?P<meeting_id>\d+)/dashboard/groups/scenarios/$', 'factors_groups_scenarios', name='factors_groups_scenarios'),
    url(r'^(?P<meeting_id>\d+)/dashboard/groups/scenarios/(?P<scenario_id>\d+)/$', 'factors_groups_scenario_chart', name='factors_groups_scenario_chart'),

    ### Decision Items Acceptance URLs
    url(r'^(?P<meeting_id>\d+)/dashboard/acceptance/$', 'features_acceptance', name='features_acceptance'),
    url(r'^(?P<meeting_id>\d+)/dashboard/acceptance/(?P<meeting_item_id>\d+)/$', 'features_acceptance_chart', name='features_acceptance_chart'),
    url(r'^(?P<meeting_id>\d+)/dashboard/acceptance/scenarios/$', 'features_acceptance_scenarios', name='features_acceptance_scenarios'),
    url(r'^(?P<meeting_id>\d+)/dashboard/acceptance/scenarios/(?P<scenario_id>\d+)/$', 'features_acceptance_scenario_chart', name='features_acceptance_scenario_chart'),

    ## Scenarios URLs
    url(r'^(?P<meeting_id>\d+)/dashboard/scenarios/add/$', 'add_scenario', name='add_scenario'),
    url(r'^(?P<meeting_id>\d+)/dashboard/scenarios/builder/$', 'scenario_builder', name='scenario_builder'),
    url(r'^(?P<meeting_id>\d+)/dashboard/scenarios/delete/$', 'delete_scenario', name='delete_scenario'),
    url(r'^(?P<meeting_id>\d+)/dashboard/scenarios/(?P<scenario_id>\d+)/$', 'details_scenario', name='details_scenario'),

    #Final Decision URLs
    url(r'^(?P<meeting_id>\d+)/decision/$', 'final_decision', name='final_decision'),
    url(r'^(?P<meeting_id>\d+)/decision/save/$', 'save_final_decision', name='save_final_decision'),

    #Meeting Settings URLs
    url(r'^(?P<meeting_id>\d+)/settings/$', 'settings', name='settings'),
    url(r'^(?P<meeting_id>\d+)/settings/items/$', 'decision_items', name='decision_items'),
    url(r'^(?P<meeting_id>\d+)/settings/stakeholders/$', 'stakeholders', name='stakeholders'),
    url(r'^(?P<meeting_id>\d+)/settings/delete/$', 'delete', name='delete'),
)
