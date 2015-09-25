# coding: utf-8

import json

from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from value.deliverables.meetings.models import Meeting
from value.deliverables.meetings.charts import Highcharts


@login_required
def features_acceptance(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    charts = meeting.meetingitem_set.all()
    stakeholder_ids = [stakeholder.stakeholder.pk for stakeholder in meeting.meetingstakeholder_set.all()]
    return render(request, 'meetings/dashboard/features_acceptance_list.html', { 
        'meeting': meeting,
        'charts': charts,
        'stakeholder_ids': stakeholder_ids,
        'chart_type': 'simple',
        'chart_uri': 'features-acceptance',
        'chart_menu_active': 'features_acceptance',
        'chart_page_title': 'Features Acceptance'
        })

@login_required
def features_acceptance_chart(request, deliverable_id, meeting_id, meeting_item_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    meeting_item = meeting.meetingitem_set.get(pk=meeting_item_id)
    chart_type = request.GET.get('chart-type', 'simple')
    stakeholder_ids = request.GET.getlist('stakeholder')
    try:
        stakeholder_ids = list(map(int, stakeholder_ids))
    except:
        pass
    chart = Highcharts()
    options = {}
    if chart_type == 'simple': 
        options = chart.features_acceptance_simple_treemap(meeting_id, meeting_item_id, stakeholder_ids)
    elif chart_type == 'detailed':
        options = chart.features_acceptance_detailed_treemap(meeting_id, meeting_item_id, stakeholder_ids)
    else:
        options = chart.features_acceptance_pie_chart_drilldown(meeting_id, meeting_item_id, stakeholder_ids)
    dump = json.dumps(options)
    if 'application/json' in request.META.get('HTTP_ACCEPT'):
        return HttpResponse(dump, content_type='application/json')
    else:
        return render(request, 'meetings/dashboard/features_acceptance_popup.html', { 
            'meeting': meeting,
            'chart': meeting_item,
            'chart_uri': 'features-acceptance',
            'chart_type': chart_type,
            'stakeholder_ids': stakeholder_ids,
            'dump': dump
            })
