# coding: utf-8

import json

from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from value.measures.models import MeasureValue
from value.deliverables.meetings.models import Meeting, Scenario, Ranking
from value.deliverables.meetings.charts import Highcharts
from value.deliverables.meetings.utils import get_stakeholders_ids, get_or_set_charts_order_session, \
        get_or_set_scenario_chars_order_session


''' Support functions '''

def get_features_chart_dict(meeting_item):
    chart_data = {
        'id': meeting_item.pk,
        'name': meeting_item.decision_item.name,
        'ranking': meeting_item.value_ranking,
        'instance': meeting_item,
        'instance_type': 'meeting_item',
        'remote': reverse('deliverables:meetings:features_chart', args=(meeting_item.meeting.deliverable.pk, meeting_item.meeting.pk, meeting_item.pk)),
        'info_remote': reverse('deliverables:details_decision_item', args=(meeting_item.meeting.deliverable.pk, meeting_item.decision_item.pk))
    }    
    return chart_data

def get_features_scenario_chart_dict(scenario):
    chart_data = {
        'id': scenario.pk,
        'name': scenario.name,
        'ranking': scenario.value_ranking,
        'instance': scenario,
        'instance_type': 'scenario',
        'remote': reverse('deliverables:meetings:features_scenario_chart', args=(scenario.meeting.deliverable.pk, scenario.meeting.pk, scenario.pk)),
        'info_remote': reverse('deliverables:meetings:details_scenario', args=(scenario.meeting.deliverable.pk, scenario.meeting.pk, scenario.pk))
    }
    return chart_data


''' Views '''

@login_required
def features(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    order = get_or_set_charts_order_session(request, meeting, 'factors_comparison_order')
    charts = map(get_features_chart_dict, meeting.get_ordered_meeting_items(order))
    stakeholder_ids = get_stakeholders_ids(meeting)
    return render(request, 'meetings/dashboard/factors_comparison/list.html', { 
        'meeting': meeting,
        'charts': charts,
        'stakeholder_ids': stakeholder_ids,
        'chart_type': 'stacked_bars',
        'chart_menu_active': 'features',
        'chart_page_title': 'Factors Comparison',
        'order': order
        })

@login_required
def features_chart(request, deliverable_id, meeting_id, meeting_item_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    meeting_item = meeting.meetingitem_set.get(pk=meeting_item_id)
    chart_type = request.GET.get('chart-type')
    stakeholders = request.GET.getlist('stakeholder')
    stakeholder_ids = get_stakeholders_ids(meeting, stakeholders)
    options = Highcharts().factors_comparison(meeting_id, meeting_item_id, chart_type, stakeholder_ids)
    dump = json.dumps(options)
    chart = get_features_chart_dict(meeting_item)
    if 'application/json' in request.META.get('HTTP_ACCEPT'):
        return HttpResponse(dump, content_type='application/json')
    else:
        return render(request, 'meetings/dashboard/factors_comparison/popup.html', { 
            'meeting': meeting,
            'chart': chart,
            'chart_type': chart_type,
            'stakeholder_ids': stakeholder_ids,
            'dump': dump
            })

@login_required
def features_scenarios(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    charts = map(get_features_scenario_chart_dict, meeting.scenarios.all())
    stakeholder_ids = get_stakeholders_ids(meeting)
    return render(request, 'meetings/dashboard/factors_comparison/scenarios.html', { 
        'meeting': meeting,
        'charts': charts,
        'chart_type': 'stacked_bars',
        'stakeholder_ids': stakeholder_ids,
        'chart_menu_active': 'features'
        })

@login_required
def features_scenario_chart(request, deliverable_id, meeting_id, scenario_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    chart_type = request.GET.get('chart-type')
    stakeholders = request.GET.getlist('stakeholder')
    stakeholder_ids = get_stakeholders_ids(meeting, stakeholders)
    options = Highcharts().factors_comparison_scenario(meeting, scenario, chart_type, stakeholder_ids)
    dump = json.dumps(options)
    chart = get_features_scenario_chart_dict(scenario)

    if 'application/json' in request.META.get('HTTP_ACCEPT'):
        return HttpResponse(dump, content_type='application/json')
    else:
        return render(request, 'meetings/dashboard/factors_comparison/popup.html', { 
            'meeting': meeting,
            'chart': chart,
            'chart_type': chart_type,
            'stakeholder_ids': stakeholder_ids,
            'dump': dump
            })
