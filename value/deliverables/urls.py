from django.conf.urls import patterns, include, url

urlpatterns = patterns('value.deliverables.views',
    url(r'^$', 'index', name='index'),
    url(r'^new/$', 'new', name='new'),
    url(r'^import-decision-items/$', 'import_decision_items', name='import_decision_items'),
    url(r'^(?P<deliverable_id>\d+)/$', 'deliverable', name='deliverable'),
    url(r'^(?P<deliverable_id>\d+)/delete/$', 'delete', name='delete'),
    url(r'^(?P<deliverable_id>\d+)/transfer/$', 'transfer', name='transfer'),
    
    url(r'^(?P<deliverable_id>\d+)/stakeholders/$', 'stakeholders', name='stakeholders'),
    url(r'^(?P<deliverable_id>\d+)/stakeholders/load-available/$', 'load_available_stakeholders', name='load_available_stakeholders'),
    url(r'^(?P<deliverable_id>\d+)/stakeholders/add/$', 'add_stakeholders', name='add_stakeholders'),
    url(r'^(?P<deliverable_id>\d+)/stakeholders/remove/$', 'remove_stakeholder', name='remove_stakeholder'),

    url(r'^(?P<deliverable_id>\d+)/decision-items/$', 'decision_items', name='decision_items'),
    url(r'^(?P<deliverable_id>\d+)/decision-items/save-import/$', 'save_imported_decision_items', name='save_imported_decision_items'),
    url(r'^(?P<deliverable_id>\d+)/decision-items/add/$', 'add_decision_item', name='add_decision_item'),
    url(r'^(?P<deliverable_id>\d+)/decision-items/(?P<decision_item_id>\d+)/$', 'edit_decision_item', name='edit_decision_item'),
    url(r'^(?P<deliverable_id>\d+)/decision-items/(?P<decision_item_id>\d+)/delete/$', 'delete_decision_item', name='delete_decision_item'),
    url(r'^(?P<deliverable_id>\d+)/decision-items/(?P<decision_item_id>\d+)/details/$', 'details_decision_item', name='details_decision_item'),
    
    url(r'^(?P<deliverable_id>\d+)/dashboard/$', 'historical_dashboard', name='historical_dashboard'),

    url(r'^(?P<deliverable_id>\d+)/settings/$', 'settings', name='settings'),

    url(r'(?P<deliverable_id>\d+)/meetings/', include('value.deliverables.meetings.urls', namespace='meetings')),
)
