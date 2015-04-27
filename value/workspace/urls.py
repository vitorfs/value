from django.conf.urls import patterns, include, url

urlpatterns = patterns('value.workspace.views',
    url(r'^$', 'index', name='index'),
    url(r'^new/$', 'new', name='new'),
    url(r'^(\d+)/$', 'instance', name='instance'),
    url(r'^(\d+)/evaluate/$', 'evaluate', name='evaluate'),
    url(r'^(\d+)/evaluate/save/$', 'save_evaluation', name='save_evaluation'),
    url(r'^(\d+)/stakeholders/$', 'stakeholders', name='stakeholders'),
)
