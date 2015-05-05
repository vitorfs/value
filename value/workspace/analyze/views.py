import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from value.factors.models import Factor
from value.measures.models import Measure, MeasureValue
from value.workspace.models import Instance, InstanceItem, InstanceItemEvaluation
from value.workspace.analyze.charts import Highcharts

@login_required
def index(request, instance_id):
    instance = get_object_or_404(Instance, pk=instance_id)
    chart = Highcharts()
    options = chart.factors_usage_pie_chart(instance)
    dump = json.dumps(options)

    if 'application/json' in request.META.get('HTTP_ACCEPT'):
        return HttpResponse(dump, content_type='application/json')
    else:
        return render(request, 'workspace/analyze/index.html', { 
            'instance' : instance, 
            'dump' : dump,
            'chart_menu_active': 'factors_usage'
            })

@login_required
def features(request, instance_id):
    instance = get_object_or_404(Instance, pk=instance_id)
    charts = instance.get_items()
    return render(request, 'workspace/analyze/features.html', { 
        'instance' : instance,
        'charts' : charts,
        'chart_uri': 'features',
        'chart_menu_active' : 'features',
        'chart_page_title' : 'Features Selection'
        })

@login_required
def features_chart(request, instance_id, item_id):
    chart_type = request.GET.get('chart')
    chart = Highcharts()
    options = chart.features_selection_stacked_chart(instance_id, item_id, chart_type)
    dump = json.dumps(options)
    return HttpResponse(dump, content_type='application/json')


@login_required
def features_acceptance(request, instance_id):
    instance = get_object_or_404(Instance, pk=instance_id)
    charts = instance.get_items()
    return render(request, 'workspace/analyze/features_acceptance.html', { 
        'instance' : instance,
        'charts' : charts,
        'chart_uri': 'features-acceptance',
        'chart_menu_active' : 'features_acceptance',
        'chart_page_title' : 'Features Acceptance'
        })

@login_required
def features_acceptance_chart(request, instance_id, item_id):
    chart_type = request.GET.get('chart', 'simple')
    chart = Highcharts()

    options = {}

    if chart_type == 'simple': 
        options = chart.features_acceptance_simple_treemap(instance_id, item_id)
    elif chart_type == 'detailed':
        options = chart.features_acceptance_detailed_treemap(instance_id, item_id)
    else:
        options = chart.features_acceptance_pie_chart_drilldown(instance_id, item_id)

    dump = json.dumps(options)
    return HttpResponse(dump, content_type='application/json')
