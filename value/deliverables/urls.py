# coding: utf-8

from django.conf.urls import include, url

from value.deliverables import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.new, name='new'),
    url(r'^import-decision-items/$', views.import_decision_items, name='import_decision_items'),
    url(r'^(?P<deliverable_id>\d+)/$', views.deliverable, name='deliverable'),
    url(r'^(?P<deliverable_id>\d+)/transfer/$', views.transfer, name='transfer'),
    url(r'^(?P<deliverable_id>\d+)/stakeholders/$', views.stakeholders, name='stakeholders'),
    url(r'^(?P<deliverable_id>\d+)/stakeholders/load-available/$', views.load_available_stakeholders,
        name='load_available_stakeholders'),
    url(r'^(?P<deliverable_id>\d+)/stakeholders/add/$', views.add_stakeholders, name='add_stakeholders'),
    url(r'^(?P<deliverable_id>\d+)/stakeholders/remove/$', views.remove_stakeholder, name='remove_stakeholder'),
    url(r'^(?P<deliverable_id>\d+)/decision-items/$', views.decision_items, name='decision_items'),
    url(r'^(?P<deliverable_id>\d+)/decision-items/save-import/$', views.save_imported_decision_items,
        name='save_imported_decision_items'),
    url(r'^(?P<deliverable_id>\d+)/decision-items/add/$', views.add_decision_item, name='add_decision_item'),
    url(r'^(?P<deliverable_id>\d+)/decision-items/(?P<decision_item_id>\d+)/$', views.edit_decision_item,
        name='edit_decision_item'),
    url(r'^(?P<deliverable_id>\d+)/decision-items/(?P<decision_item_id>\d+)/delete/$', views.delete_decision_item,
        name='delete_decision_item'),
    url(r'^(?P<deliverable_id>\d+)/decision-items/(?P<decision_item_id>\d+)/details/$', views.details_decision_item,
        name='details_decision_item'),

    # JIRA Integration
    url(r'^(?P<deliverable_id>\d+)/decision-items/jira-search-issues/$', views.jira_search_issues,
        name='jira_search_issues'),
    url(r'^(?P<deliverable_id>\d+)/decision-items/jira-import-issues/$', views.jira_import_issues,
        name='jira_import_issues'),

    url(r'^(?P<deliverable_id>\d+)/dashboard/$', views.historical_dashboard, name='historical_dashboard'),
    url(r'^(?P<deliverable_id>\d+)/dashboard/progress/$', views.historical_dashboard_progress,
        name='historical_dashboard_progress'),
    url(r'^(?P<deliverable_id>\d+)/dashboard/(?P<meeting_id>\d+)/$', views.historical_dashboard_meeting,
        name='historical_dashboard_meeting'),

    url(r'^(?P<deliverable_id>\d+)/settings/$', views.settings, name='settings'),
    url(r'^(?P<deliverable_id>\d+)/settings/factors/$', views.factors_settings, name='factors_settings'),
    url(r'^(?P<deliverable_id>\d+)/settings/measure/$', views.measure_settings, name='measure_settings'),
    url(r'^(?P<deliverable_id>\d+)/settings/access/$', views.access_settings, name='access_settings'),

    url(r'(?P<deliverable_id>\d+)/meetings/', include('value.deliverables.meetings.urls', namespace='meetings')),
]
