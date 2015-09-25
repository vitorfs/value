# coding: utf-8

from reportlab.graphics import renderPDF
import xml.dom.minidom
import json

from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.loader import render_to_string

from value.utils.svglib import SvgRenderer
from value.measures.models import MeasureValue
from value.deliverables.meetings.models import Meeting, Evaluation
from value.deliverables.meetings.charts import Highcharts


@login_required
def dashboard(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    chart = Highcharts()
    
    charts = []
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
    chart_data = { 'chart_id': 'factors_usage', 'chart_title': 'Factors Usage', 'chart_uri': reverse('deliverables:meetings:dashboard_factors_usage_chart', args=(deliverable_id, meeting_id,)) }
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
    chart_data = { 'chart_id': 'stakeholders_input', 'chart_title': 'Stakeholders Input', 'chart_uri': reverse('deliverables:meetings:dashboard_stakeholders_input_chart', args=(deliverable_id, meeting_id,)) }
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
    return render(request, 'meetings/dashboard/value_ranking.html', { 
            'meeting': meeting,
            'chart_page_title': 'Value Ranking',
            'chart_menu_active': 'value_ranking',
            'chart_uri': 'value-ranking',
            'dump': dump
            })

@login_required
def decision_items_overview(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    chart_type = request.GET.get('chart-type', 'stacked_columns')
    chart = Highcharts()
    if 'stakeholder' in request.GET:
        stakeholder_ids = request.GET.getlist('stakeholder')
        try:
            stakeholder_ids = list(map(int, stakeholder_ids))
        except:
            pass
    else:
        stakeholder_ids = [stakeholder.stakeholder.pk for stakeholder in meeting.meetingstakeholder_set.all()]
    options = chart.decision_items_overview(meeting, chart_type, stakeholder_ids)
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
            'chart_uri': 'decision-items-overview',
            'chart_menu_active': 'decision_items_overview',
            'chart_page_title': 'Decision Items Overview'
            })

@login_required
def features_comparison(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    stakeholder_ids = [stakeholder.stakeholder.pk for stakeholder in meeting.meetingstakeholder_set.all()]
    evaluations = Evaluation.get_evaluations_by_meeting(meeting).filter(user_id__in=stakeholder_ids)
    measure = evaluations[0].measure
    charts = measure.measurevalue_set.all()
    return render(request, 'meetings/dashboard/decision_items_comparison_list.html', { 
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
    stakeholder_ids = request.GET.getlist('stakeholder')
    try:
        stakeholder_ids = list(map(int, stakeholder_ids))
    except:
        pass
    chart = Highcharts()
    options = chart.feature_comparison_bar_chart(meeting, measure_value, stakeholder_ids)
    dump = json.dumps(options)
    chart_data = MeasureValue.objects.get(id=measure_value_id)
    if 'application/json' in request.META.get('HTTP_ACCEPT'):
        return HttpResponse(dump, content_type='application/json')
    else:
        return render(request, 'meetings/dashboard/decision_items_comparison_popup.html', { 
            'meeting': meeting, 
            'dump': dump,
            'chart': chart_data,
            'stakeholder_ids': stakeholder_ids,
            'chart_uri': 'features-comparison',
            'chart_menu_active': 'features_comparison',
            'chart_page_title': 'Features Comparison'
            })

@login_required
def download(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    response = HttpResponse(content_type='application/pdf')
    try:
        svg = request.POST.get('svg')
        doc = xml.dom.minidom.parseString(svg.encode('utf-8'))
        svg = doc.documentElement
        svgRenderer = SvgRenderer()
        svgRenderer.render(svg)
        drawing = svgRenderer.finish()
        pdf = renderPDF.drawToString(drawing)
        response.write(pdf)     
    except:
        pass
    response['Content-Disposition'] = 'attachment; filename=dashboard.pdf'
    return response
