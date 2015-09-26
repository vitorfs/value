# coding: utf-8

import json

from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.loader import render_to_string

from value.deliverables.meetings.models import Meeting, Scenario
from value.deliverables.meetings.charts import Highcharts
from value.deliverables.meetings.forms import FactorsGroupsScenarioBuilderForm
from value.deliverables.meetings.utils import get_stakeholders_ids, get_or_set_charts_order_session, \
        get_or_set_scenario_chars_order_session


''' Support functions '''

def get_factors_groups_chart_dict(meeting_item):
    chart_data = { 
        'id': meeting_item.pk,
        'name': meeting_item.decision_item.name,
        'ranking': meeting_item.value_ranking,
        'instance': meeting_item,
        'instance_type': 'meeting_item',
        'remote': reverse('deliverables:meetings:factors_groups_chart', args=(meeting_item.meeting.deliverable.pk, meeting_item.meeting.pk, meeting_item.pk)),
        'info_remote': reverse('deliverables:details_decision_item', args=(meeting_item.meeting.deliverable.pk, meeting_item.decision_item.pk))
    }
    return chart_data

def get_factors_groups_scenario_chart_dict(scenario):
    chart_data = {
        'id': scenario.pk,
        'name': scenario.name,
        'ranking': scenario.value_ranking,
        'instance': scenario,
        'instance_type': 'scenario',
        'remote': reverse('deliverables:meetings:factors_groups_scenario_chart', args=(scenario.meeting.deliverable.pk, scenario.meeting.pk, scenario.pk)),
        'info_remote': reverse('deliverables:meetings:details_scenario', args=(scenario.meeting.deliverable.pk, scenario.meeting.pk, scenario.pk))
    }
    return chart_data


''' Views '''

@login_required
def factors_groups(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    order = get_or_set_charts_order_session(request, meeting, 'factors_groups_comparison_order')
    charts = map(get_factors_groups_chart_dict, meeting.get_ordered_meeting_items(order))
    stakeholder_ids = get_stakeholders_ids(meeting)
    return render(request, 'meetings/dashboard/factors_groups_comparison/list.html', { 
            'meeting': meeting,
            'charts': charts,
            'stakeholder_ids': stakeholder_ids,
            'chart_menu_active': 'factors_groups',
            'chart_page_title': 'Factors Groups Comparison',
            'order': order
            })

@login_required
def factors_groups_chart(request, deliverable_id, meeting_id, meeting_item_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    meeting_item = meeting.meetingitem_set.get(pk=meeting_item_id)
    stakeholders = request.GET.getlist('stakeholder')
    stakeholder_ids = get_stakeholders_ids(meeting, stakeholders)
    options = Highcharts().factors_groups(meeting_item, stakeholder_ids)
    dump = json.dumps(options)
    if 'application/json' in request.META.get('HTTP_ACCEPT'):
        return HttpResponse(dump, content_type='application/json')
    else:
        chart = get_factors_groups_chart_dict(meeting_item)
        return render(request, 'meetings/dashboard/factors_groups_comparison/popup.html', { 
            'meeting': meeting,
            'chart': chart,
            'chart_uri': 'features',
            'stakeholder_ids': stakeholder_ids,
            'dump': dump
            })

@login_required
def factors_groups_scenarios(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    charts = map(get_factors_groups_scenario_chart_dict, meeting.scenarios.all())
    stakeholder_ids = get_stakeholders_ids(meeting)
    return render(request, 'meetings/dashboard/factors_groups_comparison/scenarios.html', { 
        'meeting': meeting,
        'charts': charts,
        'stakeholder_ids': stakeholder_ids,
        'chart_menu_active': 'factors_groups'
        })

@login_required
def factors_groups_scenario_chart(request, deliverable_id, meeting_id, scenario_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    stakeholders = request.GET.getlist('stakeholder')
    stakeholder_ids = get_stakeholders_ids(meeting, stakeholders)
    options = Highcharts().factors_groups_scenario(meeting, scenario, stakeholder_ids)
    dump = json.dumps(options)
    chart = get_factors_groups_scenario_chart_dict(scenario)
    if 'application/json' in request.META.get('HTTP_ACCEPT'):
        return HttpResponse(dump, content_type='application/json')
    else:
        return render(request, 'meetings/dashboard/factors_groups_comparison/popup.html', { 
            'meeting': meeting,
            'chart': chart,
            'stakeholder_ids': stakeholder_ids,
            'dump': dump
            })

@login_required
def factors_groups_scenario_builder(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    form = FactorsGroupsScenarioBuilderForm(initial={ 'meeting': meeting, 'category': Scenario.FACTORS_GROUPS })
    context = RequestContext(request, { 'form': form })
    json_context = dict()
    json_context['form'] = render_to_string('includes/form_vertical.html', context)
    return HttpResponse(json.dumps(json_context), content_type='application/json')
