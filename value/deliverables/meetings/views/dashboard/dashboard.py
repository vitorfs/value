# coding: utf-8

import json
import itertools
import operator

from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _

from value.measures.models import MeasureValue
from value.deliverables.decorators import user_is_manager
from value.deliverables.meetings.agreement_matrix import StakeholdersAgreement
from value.deliverables.meetings.charts import Highcharts
from value.deliverables.meetings.decorators import meeting_is_analysing_or_closed
from value.deliverables.meetings.models import Meeting
from value.deliverables.meetings.utils import *


@login_required
def dashboard(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)

    charts = list()
    charts.append({
        'chart_id': 'factors_usage',
        'chart_title': 'Factors Usage',
        'chart_uri': reverse('deliverables:meetings:dashboard_factors_usage_chart', args=(
            deliverable_id,
            meeting_id,)
        )
    })
    charts.append({
        'chart_id': 'stakeholders_input',
        'chart_title': 'Stakeholders Input',
        'chart_uri': reverse('deliverables:meetings:dashboard_stakeholders_input_chart', args=(
            deliverable_id,
            meeting_id,)
        )
    })

    if meeting.is_ongoing():
        return render(request, 'meetings/dashboard/dashboard_closed.html', {
            'meeting': meeting,
            'charts': charts
        })
    else:
        return redirect('deliverables:meetings:decision_items_overview', meeting.deliverable.pk, meeting.pk)


@login_required
@user_is_manager
def dashboard_factors_usage_chart(request, deliverable_id, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id)
    chart = Highcharts()
    options = chart.factors_usage_bar_chart(meeting)
    dump = json.dumps(options)
    chart_data = {
        'chart_id': 'factors_usage',
        'chart_title': _('Factors Usage'),
        'chart_uri': reverse('deliverables:meetings:dashboard_factors_usage_chart', args=(deliverable_id, meeting_id,))
    }
    if 'application/json' in request.META.get('HTTP_ACCEPT'):
        return HttpResponse(dump, content_type='application/json')
    else:
        return render(request, 'meetings/dashboard/dashboard_popup.html', {
            'meeting': meeting,
            'chart': chart_data,
            'dump': dump})


@login_required
@user_is_manager
def dashboard_stakeholders_input_chart(request, deliverable_id, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id)
    chart = Highcharts()
    options = chart.stakeholders_input_bar_chart(meeting)
    dump = json.dumps(options)
    chart_data = {
        'chart_id': 'stakeholders_input',
        'chart_title': _('Stakeholders Input'),
        'chart_uri': reverse(
            'deliverables:meetings:dashboard_stakeholders_input_chart', args=(
                deliverable_id,
                meeting_id
            )
        )
    }
    if 'application/json' in request.META.get('HTTP_ACCEPT'):
        return HttpResponse(dump, content_type='application/json')
    else:
        return render(request, 'meetings/dashboard/dashboard_popup.html', {
            'meeting': meeting,
            'chart': chart_data,
            'dump': dump})


''' Value Ranking '''


def get_value_ranking_chart_dict(meeting):
    chart_data = {
        'id': 'value-ranking',
        'name': _('Value Ranking'),
        'remote': reverse('deliverables:meetings:value_ranking', args=(meeting.deliverable.pk, meeting.pk))
    }
    return chart_data


@login_required
@meeting_is_analysing_or_closed
def value_ranking(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    options = Highcharts().value_ranking(meeting)
    dump = json.dumps(options)
    chart = get_value_ranking_chart_dict(meeting)
    if 'application/json' in request.META.get('HTTP_ACCEPT'):
        return HttpResponse(dump, content_type='application/json')
    else:
        template_name = 'meetings/dashboard/value_ranking/list.html'
        if 'popup' in request.GET:
            template_name = 'meetings/dashboard/value_ranking/popup.html'
        return render(request, template_name, {
            'meeting': meeting,
            'chart_menu_active': 'value_ranking',
            'chart_page_title': _('Value Ranking'),
            'chart': chart,
            'dump': dump})


''' Decision Items Overview '''


def get_decision_items_overview_chart_dict(meeting):
    chart_data = {
        'id': 'meeting-overview',
        'name': _('Decision Items Overview'),
        'remote': reverse('deliverables:meetings:decision_items_overview', args=(meeting.deliverable.pk, meeting.pk))
    }
    return chart_data


@login_required
@meeting_is_analysing_or_closed
def decision_items_overview(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)

    chart_type = get_or_set_bar_chart_type_session(request, 'decision_items_overview_chart_type', 'stacked_columns')
    chart_types_options = get_bar_chart_types_dict()

    if 'stakeholder' in request.GET:
        stakeholders = request.GET.getlist('stakeholder')
        stakeholder_ids = get_stakeholders_ids(meeting, stakeholders)
    else:
        stakeholder_ids = get_stakeholders_ids(meeting)

    options = Highcharts().decision_items_overview(meeting, chart_type, stakeholder_ids)
    dump = json.dumps(options)
    chart = get_decision_items_overview_chart_dict(meeting)

    if 'application/json' in request.META.get('HTTP_ACCEPT'):
        return HttpResponse(dump, content_type='application/json')
    else:
        template_name = 'meetings/dashboard/decision_items_overview/list.html'
        if 'popup' in request.GET:
            template_name = 'meetings/dashboard/decision_items_overview/popup.html'
        return render(request, template_name, {
            'meeting': meeting,
            'chart_menu_active': 'decision_items_overview',
            'chart_page_title': _('Decision Items Overview'),
            'dump': dump,
            'stakeholder_ids': stakeholder_ids,
            'chart_type': chart_type,
            'chart_types_options': chart_types_options,
            'chart': chart})


@login_required
@meeting_is_analysing_or_closed
def features_comparison(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    stakeholder_ids = get_stakeholders_ids(meeting)
    measure = meeting.measure
    charts = measure.measurevalue_set.all()
    return render(request, 'meetings/dashboard/decision_items_comparison/list.html', {
        'meeting': meeting,
        'charts': charts,
        'stakeholder_ids': stakeholder_ids,
        'chart_uri': 'measures',
        'chart_menu_active': 'features_comparison',
        'chart_page_title': _('Decision Items Comparison')})


@login_required
@meeting_is_analysing_or_closed
def features_comparison_chart(request, deliverable_id, meeting_id, measure_value_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    measure_value = MeasureValue.objects.get(pk=measure_value_id)

    stakeholders = request.GET.getlist('stakeholder')

    stakeholder_ids = get_stakeholders_ids(meeting, stakeholders)
    options = Highcharts().feature_comparison_bar_chart(meeting, measure_value, stakeholder_ids)

    dump = json.dumps(options)
    chart = MeasureValue.objects.get(id=measure_value_id)

    if 'application/json' in request.META.get('HTTP_ACCEPT'):
        return HttpResponse(dump, content_type='application/json')
    else:
        return render(request, 'meetings/dashboard/decision_items_comparison/popup.html', {
            'meeting': meeting,
            'dump': dump,
            'chart': chart,
            'stakeholder_ids': stakeholder_ids,
            'chart_uri': 'measures',
            'chart_menu_active': 'features_comparison',
            'chart_page_title': _('Features Comparison')})


''' Stakeholders Agreement '''
@login_required
@meeting_is_analysing_or_closed
def stakeholders_agreement(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    return render(request, 'meetings/dashboard/stakeholders_agreement.html', {
        'meeting': meeting,
        'stakeholders_agreement': StakeholdersAgreement(meeting),
        'active_tab': 'raw'
    })

@login_required
@meeting_is_analysing_or_closed
def stakeholders_agreement_grouped(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    return render(request, 'meetings/dashboard/stakeholders_agreement.html', {
        'meeting': meeting,
        'stakeholders_agreement': StakeholdersAgreement(meeting, group_measures=True),
        'active_tab': 'grouped'
    })

''' Stakeholders Individual Opinion '''
@login_required
@meeting_is_analysing_or_closed
def stakeholders_opinion(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    return render(request, 'meetings/dashboard/stakeholders_opinion.html', {
        'meeting': meeting,
        'stakeholders_agreement': StakeholdersAgreement(meeting),
        'active_tab': 'raw'
    })
