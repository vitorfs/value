import json
import operator
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from value.workspace.models import Instance, InstanceItem, InstanceItemEvaluation
from value.factors.models import Factor
from value.measures.models import Measure, MeasureValue
from django.template.loader import render_to_string

@login_required
def index(request, instance_id):
    instance = get_object_or_404(Instance, pk=instance_id)
    evaluations = InstanceItemEvaluation.get_evaluations_by_instance(instance)
    factors = Factor.get_factors()
    data = []
    for factor in factors:
        data.append([factor.name, evaluations.filter(factor=factor).exclude(measure_value__description='N/A').count()])
    dump = json.dumps(data)
    return render(request, 'workspace/analyze/index.html', { 'instance' : instance, 'data' : dump })

@login_required
def features(request, instance_id):
    instance = get_object_or_404(Instance, pk=instance_id)
    charts = instance.get_items()
    return render(request, 'workspace/analyze/features.html', { 
        'instance' : instance,
        'charts' : charts,
        'chart_menu_active' : 'features',
        'chart_page_title' : 'Features Selection'
        })

@login_required
def features_chart(request, instance_id, item_id):

    chart_type = request.GET.get('chart', 'bar')

    if chart_type not in ['bar', 'column']:
        chart_type = 'bar'

    instance = get_object_or_404(Instance, pk=instance_id)
    item = get_object_or_404(InstanceItem, pk=item_id)

    evaluations = InstanceItemEvaluation.get_evaluations_by_instance(instance).filter(item=item)

    if evaluations:
        data = {}

        for evaluation in evaluations:
            data[evaluation.factor.name] = {}
            for value in evaluation.factor.measure.get_values():
                data[evaluation.factor.name][value.description] = 0

        for evaluation in evaluations:
            data[evaluation.factor.name][evaluation.measure_value.description] = data[evaluation.factor.name][evaluation.measure_value.description] + 1

        sorted_data = sorted(data.items(), key=operator.itemgetter(0))

        categories = []
        for factor in sorted_data:
            categories.append(factor[0])

        measure = evaluations[0].measure

        series = []
        for value in measure.get_values():
            serie_data = []
            for factor in sorted_data:
                serie_data.append(factor[1][value.description])
            series.append({ 'name': value.description, 'data': serie_data, 'color': value.color })

        options = {
            'chart': { 'type': chart_type },
            'title': { 'text': item.name },
            'xAxis': { 'categories': categories },
            'yAxis': { 'min': 0, 'title': { 'text': 'Number of votes' } },
            'legend': { 'reversed': True },
            'plotOptions': { 'series': { 'stacking': 'normal' }},
            'series': series
        }

        dump = json.dumps(options)

        return HttpResponse(dump, content_type='application/json')

    else:

        return HttpResponse('')

@login_required
def features_acceptance(request, instance_id):
    instance = get_object_or_404(Instance, pk=instance_id)
    charts = instance.get_items()
    return render(request, 'workspace/analyze/base_charts.html', { 
        'instance' : instance,
        'charts' : charts,
        'chart_menu_active' : 'features_acceptance',
        'chart_page_title' : 'Features Acceptance'
        })

@login_required
def features_acceptance_chart(request, instance_id, item_id):
    instance = get_object_or_404(Instance, pk=instance_id)
    items = instance.get_items()
    evaluations = InstanceItemEvaluation.get_evaluations_by_instance(instance)

    feature_charts = {}

    for item in items:

        item_evaluation = InstanceItemEvaluation.get_evaluations_by_instance(instance).filter(item=item)

        vqs = item_evaluation.values('measure_value__description', 'measure_value__color').annotate(value=Count('measure_value__description')).order_by()
        data = [kv for kv in vqs]

        for d in data:
            d['name'] = d.pop('measure_value__description')
            d['color'] = d.pop('measure_value__color')

        highchart_data = {
            'series': [{
                'type': 'treemap',
                'layoutAlgorithm': 'stripes',
                'alternateStartingDirection': True,
                'levels': [{
                    'level': 1,
                    'layoutAlgorithm': 'sliceAndDice',
                    'dataLabels': {
                        'enabled': True,
                        'align': 'left',
                        'verticalAlign': 'top',
                        'style': { 'fontSize': '15px', 'fontWeight': 'bold' }
                    }
                }],
                'data': data
            }],
            'title': { 'text': item.name }
        }

        dump = json.dumps(highchart_data)
        feature_charts[item.id] = dump

    return render(request, 'workspace/analyze/features_acceptance.html', { 'instance' : instance, 'feature_charts' : feature_charts })

@login_required
def features_acceptance_factors(request, instance_id):
    instance = get_object_or_404(Instance, pk=instance_id)
    items = instance.get_items()
    evaluations = InstanceItemEvaluation.get_evaluations_by_instance(instance)

    feature_charts = {}

    for item in items:
        item_evaluation = InstanceItemEvaluation.get_evaluations_by_instance(instance).filter(item=item)

        vqs = item_evaluation.order_by('measure_value__description', 'measure_value__id', 'measure_value__color').distinct('measure_value__description', 'measure_value__id', 'measure_value__color').values('measure_value__description', 'measure_value__id', 'measure_value__color')
        groups = [kv for kv in vqs]
        for g in groups:
            g['id'] = g['measure_value__description']
            g['name'] = g['measure_value__description']
            del g['measure_value__description']
            g['color'] = g.pop('measure_value__color')


        vqs = item_evaluation.values('measure_value__description', 'factor__name').annotate(value=Count('measure_value__description')).order_by()
        data = [kv for kv in vqs]
        for d in data:
            d['name'] = d.pop('factor__name')
            d['parent'] = d.pop('measure_value__description')

        data = groups + data

        highchart_data = {
            'series': [{
                'type': 'treemap',
                'layoutAlgorithm': 'stripes',
                'alternateStartingDirection': True,
                'levels': [{
                    'level': 1,
                    'layoutAlgorithm': 'sliceAndDice',
                    'dataLabels': {
                        'enabled': True,
                        'align': 'left',
                        'verticalAlign': 'top',
                        'style': { 'fontSize': '15px', 'fontWeight': 'bold' }
                    }
                }],
                'data': data
            }],
            'title': { 'text': item.name }
        }

        dump = json.dumps(highchart_data)
        feature_charts[item.id] = dump

    return render(request, 'workspace/analyze/features_acceptance_factors.html', { 'instance' : instance, 'feature_charts' : feature_charts })

@login_required
def features_drilldown(request, instance_id):
    instance = get_object_or_404(Instance, pk=instance_id)
    items = instance.get_items()
    evaluations = InstanceItemEvaluation.get_evaluations_by_instance(instance)

    feature_charts = {}

    for item in items:

        item_evaluation = InstanceItemEvaluation.get_evaluations_by_instance(instance).filter(item=item)

        vqs = item_evaluation.values('measure_value__description', 'measure_value__color').annotate(y=Count('measure_value__description')).order_by('y')
        series = [kv for kv in vqs]
        for serie in series:
            serie['name'] = serie['measure_value__description']
            serie['drilldown'] = serie['measure_value__description']
            del serie['measure_value__description']
            serie['color'] = serie.pop('measure_value__color')

        vqs = item_evaluation.order_by('measure_value__id', 'measure_value__description').distinct('measure_value__id', 'measure_value__description').values('measure_value__id', 'measure_value__description')

        drilldownSeries = []

        for v in vqs:
            vqs = item_evaluation.filter(measure_value__id=v['measure_value__id']).values('measure_value__description', 'factor__name').annotate(y=Count('measure_value__description')).order_by('y')
            data = []
            for value in vqs:
                data.append([value['factor__name'], value['y']])

            drilldown = {
                'data': data,
                'id': v['measure_value__description'],
                'name': v['measure_value__description']
            }

            drilldownSeries.append(drilldown)

        highchart_data = {
                'chart': { 'type': 'pie' },
                'title': { 'text': item.name },
                'subtitle': { 'text': 'Stakeholders opinion. Click the slices to view value factors.' },
                'plotOptions': { 'series': { 'dataLabels': { 'enabled': True, 'format': '{point.name}: {point.y} votes' } } },
                'tooltip': {
                    'headerFormat': '<span style="font-size:11px">{series.name}</span><br>',
                    'pointFormat': '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b><br/>'
                },
                'series': [{
                    'name': 'Votes',
                    'colorByPoint': True,
                    'data': series
                }],
                'drilldown': {
                    'series': drilldownSeries
                }
            }

        dump = json.dumps(highchart_data)
        feature_charts[item.id] = dump

    return render(request, 'workspace/analyze/features_drilldown.html', { 'instance' : instance, 'feature_charts' : feature_charts })
