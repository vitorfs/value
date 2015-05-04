from django.conf.urls import patterns, include, url

urlpatterns = patterns('value.workspace.views',
    url(r'^$', 'index', name='index'),
    url(r'^new/$', 'new', name='new'),
    url(r'^(?P<instance_id>\d+)/$', 'instance', name='instance'),
    url(r'^(?P<instance_id>\d+)/evaluate/$', 'evaluate', name='evaluate'),
    url(r'^(?P<instance_id>\d+)/evaluate/save/$', 'save_evaluation', name='save_evaluation'),
    url(r'^(?P<instance_id>\d+)/stakeholders/$', 'stakeholders', name='stakeholders'),
    url(r'^(?P<instance_id>\d+)/backlog/$', 'backlog', name='backlog'),
    url(r'(?P<instance_id>\d+)/analyze/', include('value.workspace.analyze.urls', namespace='analyze')),
)
