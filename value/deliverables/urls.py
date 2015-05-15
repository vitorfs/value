from django.conf.urls import patterns, include, url

urlpatterns = patterns('value.deliverables.views',
    url(r'^$', 'index', name='index'),
    url(r'^new/$', 'new', name='new'),
    url(r'^(?P<deliverable_id>\d+)/$', 'deliverable', name='deliverable'),
    url(r'^(?P<deliverable_id>\d+)/stakeholders/$', 'stakeholders', name='stakeholders'),
    url(r'^(?P<deliverable_id>\d+)/decision-items/$', 'decision_items', name='decision_items'),
    url(r'(?P<deliverable_id>\d+)/meetings/', include('value.deliverables.meetings.urls', namespace='meetings')),
)
