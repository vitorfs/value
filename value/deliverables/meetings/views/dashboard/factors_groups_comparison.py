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
from value.deliverables.meetings.utils import get_stakeholders_ids


@login_required
def factors_groups(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    charts = [{ 
        'id': item.pk,
        'name': item.decision_item.name, 
        'remote': reverse('deliverables:meetings:factors_groups_chart', args=(meeting.deliverable.pk, meeting.pk, item.pk)),
        'info_remote': reverse('deliverables:details_decision_item', args=(meeting.deliverable.pk, item.decision_item.pk))
    } for item in meeting.meetingitem_set.all()]
    stakeholder_ids = get_stakeholders_ids(meeting)
    return render(request, 'meetings/dashboard/factors_groups_comparison/list.html', { 
            'meeting': meeting,
            'charts': charts,
            'stakeholder_ids': stakeholder_ids,
            'chart_menu_active': 'factors_groups',
            'chart_page_title': 'Factors Groups Comparison',
            'type': 'meeting_item'
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
        chart = { 
            'id': meeting_item.pk,
            'name': meeting_item.decision_item.name, 
            'remote': reverse('deliverables:meetings:factors_groups_chart', args=(meeting.deliverable.pk, meeting.pk, meeting_item.pk)),
            'info_remote': reverse('deliverables:details_decision_item', args=(meeting.deliverable.pk, meeting_item.decision_item.pk))
        }
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
    charts = [{
        'id': scenario.pk,
        'name': scenario.name,
        'remote': reverse('deliverables:meetings:factors_groups_scenario_chart', args=(meeting.deliverable.pk, meeting.pk, scenario.pk)),
        'info_remote': reverse('deliverables:meetings:details_scenario', args=(meeting.deliverable.pk, meeting.pk, scenario.pk))
    } for scenario in meeting.scenarios.all()]
    stakeholder_ids = get_stakeholders_ids(meeting)
    return render(request, 'meetings/dashboard/factors_groups_comparison/scenarios.html', { 
        'meeting': meeting,
        'charts': charts,
        'stakeholder_ids': stakeholder_ids,
        'chart_menu_active': 'factors_groups',
        'type': 'scenario'
        })

@login_required
def factors_groups_scenario_chart(request, deliverable_id, meeting_id, scenario_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    stakeholders = request.GET.getlist('stakeholder')
    stakeholder_ids = get_stakeholders_ids(meeting, stakeholders)
    options = Highcharts().factors_groups_scenario(meeting, scenario, stakeholder_ids)
    dump = json.dumps(options)

    chart = {
        'id': scenario.pk,
        'name': scenario.name,
        'remote': reverse('deliverables:meetings:factors_groups_scenario_chart', args=(meeting.deliverable.pk, meeting.pk, scenario.pk))
    }

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
