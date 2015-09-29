# coding: utf-8

import json

from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from value.deliverables.meetings.models import Meeting, Scenario
from value.deliverables.meetings.charts import Highcharts
from value.deliverables.meetings.utils import *


''' Support functions'''

def get_features_acceptance_chart_dict(meeting_item):
    chart_data = {
        'id': meeting_item.pk,
        'name': meeting_item.decision_item.name,
        'ranking': meeting_item.value_ranking,
        'instance': meeting_item,
        'instance_type': 'meeting_item',
        'remote': reverse('deliverables:meetings:features_acceptance_chart', args=(meeting_item.meeting.deliverable.pk, meeting_item.meeting.pk, meeting_item.pk)),
        'info_remote': reverse('deliverables:details_decision_item', args=(meeting_item.meeting.deliverable.pk, meeting_item.decision_item.pk))
    }    
    return chart_data

def get_features_acceptance_scenario_chart_dict(scenario):
    chart_data = {
        'id': scenario.pk,
        'name': scenario.name,
        'ranking': scenario.value_ranking,
        'instance': scenario,
        'instance_type': 'scenario',
        'remote': reverse('deliverables:meetings:features_acceptance_scenario_chart', args=(scenario.meeting.deliverable.pk, scenario.meeting.pk, scenario.pk)),
        'info_remote': reverse('deliverables:meetings:details_scenario', args=(scenario.meeting.deliverable.pk, scenario.meeting.pk, scenario.pk))
    }
    return chart_data

def get_features_acceptance_chart_options(meeting_item, stakeholder_ids, chart_type):
    charts = Highcharts()
    chart_function = charts.decision_item_acceptance_simple_treemap
    if chart_type == 'detailed':
        chart_function = charts.decision_item_acceptance_detailed_treemap
    elif chart_type == 'pie':
        chart_function = charts.decision_item_acceptance_pie_chart_drilldown
    options = chart_function(meeting_item, stakeholder_ids)
    return options

def get_features_acceptance_scenario_chart_options(scenario, stakeholder_ids, chart_type):
    charts = Highcharts()
    chart_function = charts.decision_item_acceptance_scenario_simple_treemap
    if chart_type == 'detailed':
        chart_function = charts.decision_item_acceptance_scenario_detailed_treemap
    elif chart_type == 'pie':
        chart_function = charts.decision_item_acceptance_scenario_pie_chart_drilldown
    options = chart_function(scenario, stakeholder_ids)
    return options

''' Views '''

@login_required
def features_acceptance(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)

    chart_type = get_or_set_treemap_chart_type_session(request, 'decision_items_acceptance_chart_type')
    chart_types_options = get_treemap_chart_types_dict()

    chart_order_options = get_charts_order_dict(meeting.deliverable.measure)
    order = get_or_set_charts_order_session(request, meeting, 'decision_items_acceptance_order')

    charts = map(get_features_acceptance_chart_dict, meeting.get_ordered_meeting_items(order))
    stakeholder_ids = get_stakeholders_ids(meeting)

    return render(request, 'meetings/dashboard/decision_items_acceptance/list.html', { 
        'meeting': meeting,
        'chart_menu_active': 'features_acceptance',
        'charts': charts,
        'stakeholder_ids': stakeholder_ids,
        'chart_types_options': chart_types_options,
        'chart_type': chart_type,
        'chart_order_options': chart_order_options,
        'order': order
        })

@login_required
def features_acceptance_chart(request, deliverable_id, meeting_id, meeting_item_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    meeting_item = meeting.meetingitem_set.get(pk=meeting_item_id)
    
    chart_type = request.GET.get('chart_type')
    stakeholder_ids = request.GET.getlist('stakeholder')

    chart_types_options = get_treemap_chart_types_dict()
    stakeholder_ids = get_stakeholders_ids(meeting)
    options = get_features_acceptance_chart_options(meeting_item, stakeholder_ids, chart_type)
    dump = json.dumps(options)
    chart = get_features_acceptance_chart_dict(meeting_item)

    if 'application/json' in request.META.get('HTTP_ACCEPT'):
        return HttpResponse(dump, content_type='application/json')
    else:
        return render(request, 'meetings/dashboard/decision_items_acceptance/popup.html', { 
            'meeting': meeting,
            'chart': chart,
            'chart_types_options': chart_types_options,
            'chart_type': chart_type,
            'stakeholder_ids': stakeholder_ids,
            'dump': dump
            })

@login_required
def features_acceptance_scenarios(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    
    chart_type = get_or_set_treemap_chart_type_session(request, 'decision_items_acceptance_scenario_chart_type')
    chart_types_options = get_treemap_chart_types_dict()

    chart_order_options = get_scenario_charts_order_dict(meeting.deliverable.measure)
    order = get_or_set_scenario_charts_order_session(request, meeting, 'decision_items_acceptance_scenario_order')

    charts = map(get_features_acceptance_scenario_chart_dict, meeting.get_ordered_scenarios(order))
    stakeholder_ids = get_stakeholders_ids(meeting)

    return render(request, 'meetings/dashboard/decision_items_acceptance/scenarios.html', { 
        'meeting': meeting,
        'chart_menu_active': 'features_acceptance',
        'charts': charts,
        'stakeholder_ids': stakeholder_ids,
        'scenario_category': Scenario.ACCEPTANCE,
        'chart_types_options': chart_types_options,
        'chart_type': chart_type,
        'chart_order_options': chart_order_options,
        'order': order
        })

@login_required
def features_acceptance_scenario_chart(request, deliverable_id, meeting_id, scenario_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    scenario = get_object_or_404(Scenario, pk=scenario_id)

    chart_type = request.GET.get('chart_type')
    stakeholders = request.GET.getlist('stakeholder')
    
    chart_types_options = get_treemap_chart_types_dict()
    stakeholder_ids = get_stakeholders_ids(meeting, stakeholders)
    options = get_features_acceptance_scenario_chart_options(scenario, stakeholder_ids, chart_type)
    dump = json.dumps(options)
    chart = get_features_acceptance_scenario_chart_dict(scenario)

    if 'application/json' in request.META.get('HTTP_ACCEPT'):
        return HttpResponse(dump, content_type='application/json')
    else:
        return render(request, 'meetings/dashboard/decision_items_acceptance/popup.html', { 
            'meeting': meeting,
            'chart': chart,
            'chart_types_options': chart_types_options,
            'chart_type': chart_type,
            'stakeholder_ids': stakeholder_ids,
            'dump': dump
            })
