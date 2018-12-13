# coding: utf-8

import json

from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

from value.deliverables.meetings.charts import Highcharts
from value.deliverables.meetings.models import Meeting, Scenario
from value.deliverables.meetings.forms import ScenarioForm, ScenarioBuilderForm, CompareScenarioForm
from value.deliverables.meetings.views.dashboard.factors_comparison import get_features_scenario_chart_dict
from value.deliverables.meetings.views.dashboard.factors_groups_comparison import \
    get_factors_groups_scenario_chart_dict, application_has_factors_groups
from value.deliverables.meetings.views.dashboard.decision_items_acceptance import \
    get_features_acceptance_scenario_chart_dict
from value.deliverables.meetings.utils import *


''' Support functions '''


def get_scenario_overview_chart_dict(scenario):
    chart_data = {
        'id': 'scenario-overview',
        'name': 'Scenario Overview',
        'remote': reverse(
            'deliverables:meetings:scenario_overview_chart',
            args=(scenario.meeting.deliverable.pk, scenario.meeting.pk, scenario.pk)
        )
    }
    return chart_data


def get_scenario_value_ranking_chart_dict(scenario):
    chart_data = {
        'id': 'scenario-value-ranking',
        'name': 'Scenario Value Ranking',
        'remote': reverse(
            'deliverables:meetings:scenario_value_ranking_chart',
            args=(scenario.meeting.deliverable.pk, scenario.meeting.pk, scenario.pk)
        )
    }
    return chart_data


def get_scenario_charts(scenario):
    chart_overview = get_scenario_overview_chart_dict(scenario)
    chart_overview_type = 'stacked_bars'

    chart_value_ranking = get_scenario_value_ranking_chart_dict(scenario)

    chart_factors = get_features_scenario_chart_dict(scenario)
    chart_factors['name'] = _('Factors Comparison')
    chart_factors_type = 'stacked_columns'

    chart_factors_groups = get_factors_groups_scenario_chart_dict(scenario)
    chart_factors_groups['name'] = _('Factors Group Comparison')

    chart_acceptance = get_features_acceptance_scenario_chart_dict(scenario)
    chart_acceptance['name'] = _('Decision Items Acceptance')
    chart_acceptance_type = 'simple'

    charts_data = {
        'chart_overview': chart_overview,
        'chart_overview_type': chart_overview_type,

        'chart_value_ranking': chart_value_ranking,

        'chart_factors': chart_factors,
        'chart_factors_type': chart_factors_type,

        'chart_factors_groups': chart_factors_groups,

        'chart_acceptance': chart_acceptance,
        'chart_acceptance_type': chart_acceptance_type
    }
    return charts_data


''' Views '''


@login_required
def add_scenario(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    scenario = Scenario(meeting=meeting)
    json_context = dict()
    if request.method == 'POST':
        form = ScenarioForm(request.POST, instance=scenario, prefix='add')
        is_valid = json_context['is_valid'] = form.is_valid()
        if is_valid:
            scenario = form.save()
            next = request.POST.get('next')
            if next == 'scenario_charts':
                json_context['redirect_to'] = reverse(
                    'deliverables:meetings:scenario',
                    args=(meeting.deliverable.pk, meeting.pk, scenario.pk)
                )
    else:
        form = ScenarioForm(instance=scenario, prefix='add')
    context = RequestContext(request, {'form': form})
    json_context['form'] = render_to_string('meetings/dashboard/scenarios/partial_scenario_form.html', context)
    return HttpResponse(json.dumps(json_context), content_type='application/json')


@login_required
def edit_scenario(request, deliverable_id, meeting_id, scenario_id):
    scenario = get_object_or_404(
        Scenario,
        pk=scenario_id,
        meeting_id=meeting_id,
        meeting__deliverable__id=deliverable_id
    )
    json_context = dict()
    if request.method == 'POST':
        form = ScenarioForm(request.POST, instance=scenario, prefix='edit')
        is_valid = json_context['is_valid'] = form.is_valid()
        if is_valid:
            form.save()
    else:
        form = ScenarioForm(instance=scenario, prefix='edit')
    context = RequestContext(request, {'form': form})
    json_context['form'] = render_to_string('meetings/dashboard/scenarios/partial_scenario_form.html', context)
    return HttpResponse(json.dumps(json_context), content_type='application/json')


@login_required
def scenario(request, deliverable_id, meeting_id, scenario_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    scenario = get_object_or_404(Scenario, pk=scenario_id)

    stakeholder_ids = get_stakeholders_ids(meeting)
    bar_chart_types_options = get_bar_chart_types_dict()
    treemap_chart_types_options = get_treemap_chart_types_dict()
    display_chart_factors_groups = application_has_factors_groups()

    charts_data = get_scenario_charts(scenario)
    context = {
        'meeting': meeting,
        'scenario': scenario,
        'chart_menu_active': scenario.pk,
        'delete_scenario_next': reverse('deliverables:meetings:dashboard', args=(meeting.deliverable.pk, meeting.pk)),
        'stakeholder_ids': stakeholder_ids,
        'bar_chart_types_options': bar_chart_types_options,
        'treemap_chart_types_options': treemap_chart_types_options,
        'display_chart_factors_groups': display_chart_factors_groups
    }
    context.update(charts_data)
    return render(request, 'meetings/dashboard/scenarios/list.html', context)


@login_required
def scenario_overview_chart(request, deliverable_id, meeting_id, scenario_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    scenario = get_object_or_404(Scenario, pk=scenario_id)

    chart_type = request.GET.get('chart_type')
    stakeholders = request.GET.getlist('stakeholder')

    chart_types_options = get_bar_chart_types_dict()
    stakeholder_ids = get_stakeholders_ids(meeting, stakeholders)
    options = Highcharts().decision_items_overview_scenario(scenario, chart_type, stakeholder_ids)
    dump = json.dumps(options)
    chart = get_scenario_overview_chart_dict(scenario)

    if 'application/json' in request.META.get('HTTP_ACCEPT'):
        return HttpResponse(dump, content_type='application/json')
    else:
        return render(request, 'meetings/dashboard/decision_items_overview/popup.html', {
            'meeting': meeting,
            'chart': chart,
            'chart_types_options': chart_types_options,
            'chart_type': chart_type,
            'stakeholder_ids': stakeholder_ids,
            'dump': dump
        })


@login_required
def scenario_value_ranking_chart(request, deliverable_id, meeting_id, scenario_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    scenario = get_object_or_404(Scenario, pk=scenario_id)

    options = Highcharts().value_ranking_scenario(scenario)
    dump = json.dumps(options)
    chart = get_scenario_value_ranking_chart_dict(scenario)

    if 'application/json' in request.META.get('HTTP_ACCEPT'):
        return HttpResponse(dump, content_type='application/json')
    else:
        return render(request, 'meetings/dashboard/value_ranking/popup.html', {
            'meeting': meeting,
            'chart': chart,
            'dump': dump
        })


@login_required
def scenario_details(request, deliverable_id, meeting_id, scenario_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    return render(request, 'meetings/dashboard/scenarios/scenario_details.html', {
        'meeting': meeting,
        'scenario': scenario
    })


@require_POST
@login_required
def delete_scenario(request, deliverable_id, meeting_id):
    scenario_id = request.POST.get('scenario')
    next = request.POST.get('next', reverse('deliverables:meetings:dashboard', args=(deliverable_id, meeting_id)))
    try:
        scenario = Scenario.objects.get(pk=scenario_id)
        scenario.delete()
        messages.success(request, _(u'Scenario {0} successfully deleted!').format(scenario.name))
    except Scenario.DoesNotExist:
        messages.error(request, _('An unexpected error ocurred.'))
    return redirect(next)


@login_required
def scenario_builder(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    json_context = dict()

    if request.method == 'POST':
        form = ScenarioBuilderForm(request.POST, initial={'meeting': meeting})
        is_valid = json_context['is_valid'] = form.is_valid()
        if is_valid:
            scenario = Scenario(meeting=meeting)
            scenario = scenario.build(**form.cleaned_data)
            next = request.POST.get('next')
            if next == 'scenario_charts':
                json_context['redirect_to'] = reverse(
                    'deliverables:meetings:scenario',
                    args=(meeting.deliverable.pk, meeting.pk, scenario.pk)
                )
    else:
        form = ScenarioBuilderForm(initial={'meeting': meeting})

    context = RequestContext(request, {'form': form})
    json_context['form'] = render_to_string('includes/form_vertical.html', context)
    return HttpResponse(json.dumps(json_context), content_type='application/json')


@login_required
def compare_scenario(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    json_context = dict()

    if request.method == 'POST':
        form = CompareScenarioForm(request.POST, initial={'meeting': meeting})
        is_valid = json_context['is_valid'] = form.is_valid()
        if is_valid:
            stakeholder_ids = get_stakeholders_ids(meeting)
            bar_chart_types_options = get_bar_chart_types_dict()
            treemap_chart_types_options = get_treemap_chart_types_dict()
            display_chart_factors_groups = application_has_factors_groups()
            scenarios = list()
            for scenario in form.cleaned_data['scenarios']:
                charts_data = get_scenario_charts(scenario)
                charts_data['name'] = scenario.name
                charts_data['scenario'] = scenario
                charts_data['scenario_items'] = scenario.meeting_items.order_by('-value_ranking')
                scenarios.append(charts_data)
            context = RequestContext(request, {
                'meeting': meeting,
                'stakeholder_ids': stakeholder_ids,
                'bar_chart_types_options': bar_chart_types_options,
                'treemap_chart_types_options': treemap_chart_types_options,
                'display_chart_factors_groups': display_chart_factors_groups,
                'scenarios': scenarios
            })
            json_context['html'] = render_to_string('meetings/dashboard/scenarios/partial_compare.html', context)
    else:
        form = CompareScenarioForm(initial={'meeting': meeting})

    context = RequestContext(request, {'meeting': meeting, 'form': form})
    json_context['form'] = render_to_string('meetings/dashboard/scenarios/partial_compare_form.html', context)
    return HttpResponse(json.dumps(json_context), content_type='application/json')
