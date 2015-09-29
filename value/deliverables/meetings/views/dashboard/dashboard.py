# coding: utf-8

import json

from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.loader import render_to_string

from value.measures.models import MeasureValue
from value.deliverables.meetings.models import Meeting, Evaluation
from value.deliverables.meetings.charts import Highcharts
from value.deliverables.meetings.utils import *


@login_required
def dashboard(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    chart = Highcharts()
    
    charts = list()
    charts.append({ 'chart_id': 'factors_usage', 'chart_title': 'Factors Usage', 'chart_uri': reverse('deliverables:meetings:dashboard_factors_usage_chart', args=(deliverable_id, meeting_id,)) })
    charts.append({ 'chart_id': 'stakeholders_input', 'chart_title': 'Stakeholders Input', 'chart_uri': reverse('deliverables:meetings:dashboard_stakeholders_input_chart', args=(deliverable_id, meeting_id,)) })

    return render(request, 'meetings/dashboard/dashboard_list.html', { 
        'meeting': meeting,
        'charts': charts,
        'chart_menu_active': 'overview'
        })

@login_required
def dashboard_factors_usage_chart(request, deliverable_id, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id)
    chart = Highcharts()
    options = chart.factors_usage_bar_chart(meeting)
    dump = json.dumps(options)
    chart_data = { 
        'chart_id': 'factors_usage', 
        'chart_title': 'Factors Usage', 
        'chart_uri': reverse('deliverables:meetings:dashboard_factors_usage_chart', args=(deliverable_id, meeting_id,)) 
    }
    if 'application/json' in request.META.get('HTTP_ACCEPT'):
        return HttpResponse(dump, content_type='application/json')
    else:
        return render(request, 'meetings/dashboard/dashboard_popup.html', { 
            'meeting': meeting,
            'chart': chart_data,
            'dump': dump
            })

@login_required
def dashboard_stakeholders_input_chart(request, deliverable_id, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id)
    chart = Highcharts()
    options = chart.stakeholders_input_bar_chart(meeting)
    dump = json.dumps(options)
    chart_data = { 
        'chart_id': 'stakeholders_input', 
        'chart_title': 'Stakeholders Input', 
        'chart_uri': reverse('deliverables:meetings:dashboard_stakeholders_input_chart', args=(deliverable_id, meeting_id,)) 
    }
    if 'application/json' in request.META.get('HTTP_ACCEPT'):
        return HttpResponse(dump, content_type='application/json')
    else:
        return render(request, 'meetings/dashboard/dashboard_popup.html', { 
            'meeting': meeting,
            'chart': chart_data,
            'dump': dump
            })

@login_required
def value_ranking(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    chart = Highcharts()
    options = chart.value_ranking(meeting)
    dump = json.dumps(options)
    chart_data = { 
        'chart_title': 'Value Ranking', 
    }
    if 'application/json' in request.META.get('HTTP_ACCEPT'):
        return HttpResponse(dump, content_type='application/json')
    else:
        template_name = 'meetings/dashboard/value_ranking.html'
        if 'popup' in request.GET:
            template_name = 'meetings/dashboard/dashboard_popup.html'
        return render(request, template_name, { 
            'meeting': meeting,
            'chart_page_title': 'Value Ranking',
            'chart_menu_active': 'value_ranking',
            'chart_uri': 'value-ranking',
            'chart': chart_data,
            'dump': dump
            })

@login_required
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

    if 'application/json' in request.META.get('HTTP_ACCEPT'):
        return HttpResponse(dump, content_type='application/json')
    else:
        template_name = 'meetings/dashboard/decision_items_overview.html'
        if 'popup' in request.GET:
            template_name = 'meetings/dashboard/decision_items_overview_popup.html'
        return render(request, template_name, { 
            'meeting': meeting, 
            'dump': dump,
            'stakeholder_ids': stakeholder_ids,
            'chart_type': chart_type,
            'chart_types_options': chart_types_options,
            'chart_uri': 'decision-items-overview',
            'chart_menu_active': 'decision_items_overview',
            'chart_page_title': 'Decision Items Overview'
            })

@login_required
def features_comparison(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    stakeholder_ids = get_stakeholders_ids(meeting)
    evaluations = Evaluation.get_evaluations_by_meeting(meeting).filter(user_id__in=stakeholder_ids)
    measure = meeting.deliverable.measure
    charts = measure.measurevalue_set.all()
    return render(request, 'meetings/dashboard/decision_items_comparison/list.html', { 
        'meeting': meeting, 
        'charts': charts,
        'stakeholder_ids': stakeholder_ids,
        'chart_uri': 'features-comparison',
        'chart_menu_active': 'features_comparison',
        'chart_page_title': 'Features Comparison'
        })

@login_required
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
            'chart_uri': 'features-comparison',
            'chart_menu_active': 'features_comparison',
            'chart_page_title': 'Features Comparison'
            })
