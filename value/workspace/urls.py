from django.conf.urls import patterns, include, url

urlpatterns = patterns('value.workspace.views',
    url(r'^$', 'index', name='index'),
    url(r'^new/$', 'new', name='new'),
    url(r'^(?P<instance_id>\d+)/$', 'instance', name='instance'),
    url(r'^(?P<instance_id>\d+)/decision-making/$', 'evaluate', name='evaluate'),
    url(r'^(?P<instance_id>\d+)/decision-making/save/$', 'save_evaluation', name='save_evaluation'),
    url(r'^(?P<instance_id>\d+)/stakeholders/$', 'stakeholders', name='stakeholders'),
    url(r'^(?P<instance_id>\d+)/decision-items/$', 'backlog', name='backlog'),
    url(r'^(?P<instance_id>\d+)/meetings/$', 'meetings', name='meetings'),
    url(r'^(?P<instance_id>\d+)/meetings/(?P<meeting_id>\d+)/$', 'meeting', name='meeting'),
    url(r'^(?P<instance_id>\d+)/meetings/new/$', 'new_meeting', name='new_meeting'),
    url(r'(?P<instance_id>\d+)/dashboard/', include('value.workspace.analyze.urls', namespace='analyze')),
)
