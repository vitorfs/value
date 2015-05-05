import operator
from django.db.models import Count
from value.factors.models import Factor
from value.workspace.models import Instance, InstanceItem, InstanceItemEvaluation

class Highcharts(object):

    def factors_usage_pie_chart(self, instance):
        evaluations = InstanceItemEvaluation.get_evaluations_by_instance(instance)
        factors = Factor.get_factors()
        data = []

        for factor in factors:
            data.append([factor.name, evaluations.filter(factor=factor).exclude(measure_value__description='N/A').count()])

        options = {
            'title': { 'text': '' },
            'tooltip': { 'pointFormat': '{series.name}: <strong>{point.percentage:.1f}%</strong>' },
            'plotOptions': { 
                'pie': { 
                    'allowPointSelect': True, 
                    'cursor': 'pointer',
                    'dataLabels': { 'enabled': True, 'format': '<strong>{point.name}</strong>: {point.percentage:.1f} %' }
                }
            },
            'series': [{ 'type': 'pie', 'name': 'Overall usage', 'data': data }]
        }

        return options

    def features_selection_stacked_chart(self, instance_id, item_id, chart_type):
        if chart_type not in ['bar', 'column']:
            chart_type = 'bar'

        instance = Instance.objects.get(pk=instance_id)
        item = InstanceItem.objects.get(pk=item_id)
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
                'title': { 'text': '' },
                'xAxis': { 'categories': categories },
                'yAxis': { 'min': 0, 'title': { 'text': 'Number of votes' } },
                'legend': { 'reversed': True },
                'plotOptions': { 'series': { 'stacking': 'normal' }},
                'series': series
            }

        else:
            options = {}

        return options

    def _base_treemap(self, data):
        options = {
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
            'title': { 'text': '' }
        }
        return options

    def features_acceptance_simple_treemap(self, instance_id, item_id):
        instance = Instance.objects.get(pk=instance_id)
        item = InstanceItem.objects.get(pk=item_id)
        evaluations = InstanceItemEvaluation.get_evaluations_by_instance(instance).filter(item=item)

        vqs = evaluations.values('measure_value__description', 'measure_value__color').annotate(value=Count('measure_value__description')).order_by()
        data = [kv for kv in vqs]
        for d in data:
            d['name'] = d.pop('measure_value__description')
            d['color'] = d.pop('measure_value__color')

        return self._base_treemap(data)

    def features_acceptance_detailed_treemap(self, instance_id, item_id):
        instance = Instance.objects.get(pk=instance_id)
        item = InstanceItem.objects.get(pk=item_id)
        evaluations = InstanceItemEvaluation.get_evaluations_by_instance(instance).filter(item=item)

        vqs = evaluations.order_by('measure_value__description', 'measure_value__id', 'measure_value__color').distinct('measure_value__description', 'measure_value__id', 'measure_value__color').values('measure_value__description', 'measure_value__id', 'measure_value__color')
        groups = [kv for kv in vqs]
        for g in groups:
            g['id'] = g['measure_value__description']
            g['name'] = g['measure_value__description']
            del g['measure_value__description']
            g['color'] = g.pop('measure_value__color')

        vqs = evaluations.values('measure_value__description', 'factor__name').annotate(value=Count('measure_value__description')).order_by()
        data = [kv for kv in vqs]
        for d in data:
            d['name'] = d.pop('factor__name')
            d['parent'] = d.pop('measure_value__description')

        data = groups + data

        return self._base_treemap(data)

    def features_acceptance_pie_chart_drilldown(self, instance_id, item_id):
        instance = Instance.objects.get(pk=instance_id)
        item = InstanceItem.objects.get(pk=item_id)
        evaluations = InstanceItemEvaluation.get_evaluations_by_instance(instance).filter(item=item)

        vqs = evaluations.values('measure_value__description', 'measure_value__color').annotate(y=Count('measure_value__description')).order_by('y')
        series = [kv for kv in vqs]
        for serie in series:
            serie['name'] = serie['measure_value__description']
            serie['drilldown'] = serie['measure_value__description']
            del serie['measure_value__description']
            serie['color'] = serie.pop('measure_value__color')

        vqs = evaluations.order_by('measure_value__id', 'measure_value__description').distinct('measure_value__id', 'measure_value__description').values('measure_value__id', 'measure_value__description')

        drilldownSeries = []

        for v in vqs:
            vqs = evaluations.filter(measure_value__id=v['measure_value__id']).values('measure_value__description', 'factor__name').annotate(y=Count('measure_value__description')).order_by('y')
            data = []
            for value in vqs:
                data.append([value['factor__name'], value['y']])

            drilldown = {
                'data': data,
                'id': v['measure_value__description'],
                'name': v['measure_value__description']
            }

            drilldownSeries.append(drilldown)

        options = {
                'chart': { 'type': 'pie' },
                'title': { 'text': '' },
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
        return options
