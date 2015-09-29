# coding: utf-8

import operator

from django.contrib.auth.models import User
from django.db.models import Count
from django.utils.html import escape

from value.factors.models import Factor, Group as FactorGroup
from value.deliverables.meetings.models import Meeting, MeetingItem, Evaluation
from value.deliverables.meetings.utils import get_votes_percentage


def get_stakeholders_group_names(stakeholder_ids):
    stakeholders = User.objects.filter(id__in=stakeholder_ids)
    groups = set()
    for stakeholder in stakeholders:
        for group in stakeholder.groups.all():
            groups.add(group.name)
    groups_text = u', '.join(groups)
    return escape(groups_text)


class Highcharts(object):

    def __init__(self):
        self.label_style = { 'fontSize': '13px', 'fontFamily': '"Helvetica Neue", Helvetica, Arial, sans-serif' }

    ''' Support Functions '''

    def _base_stacked_chart(self, categories, series, chart='stacked_columns'):

        chart_type = 'bar'
        stacking = None

        if chart in ['stacked_bars', 'stacked_columns',]:
            stacking = 'normal'

        if chart in ['stacked_columns', 'basic_columns',]:
            chart_type = 'column'

        options = {
            'chart': { 'type': chart_type },
            'title': { 'text': '' },
            'xAxis': { 'categories': categories },
            'yAxis': { 'min': 0, 'max': 100, 'title': { 'text': 'Percentage of evaluations' }, 'labels': { 'format': '{value}%' } },
            'legend': { 'reversed': True },
            'plotOptions': { 'series': { 'stacking': stacking }},
            'tooltip': { 'pointFormat': 'Percentage: <strong>{point.y}%</strong>' },
            'exporting': { 'enabled': False },
            'series': series
        }

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
            'exporting': { 'enabled': False },
            'title': { 'text': '' }
        }
        return options


    ''' Summary Charts '''

    def stakeholders_input_bar_chart(self, meeting):
        evaluations = Evaluation.get_evaluations_by_meeting(meeting)
        meeting_stakeholders = meeting.meetingstakeholder_set.all()
        factors = Factor.list()

        data = []

        meeting_items_count = meeting.meetingitem_set.count()
        factors_count = factors.count()

        max_input = factors_count * meeting_items_count

        for meeting_stakeholder in meeting_stakeholders:
            votes = evaluations.filter(user=meeting_stakeholder.stakeholder).count()
            percentage = get_votes_percentage(max_input, votes)
            data.append([meeting_stakeholder.stakeholder.profile.get_display_name(), percentage])

        data = sorted(data, key=operator.itemgetter(1))
        data.reverse()

        options = {
            'chart': { 'type': 'bar' },
            'title': { 'text': 'Stakeholder\'s Input' },
            'subtitle': { 'text': '100% means the stakeholder evaluated all the meeting\'s decision items.' },
            'xAxis': {
                'type': 'category',
                'labels': { 'style': self.label_style }
            },
            'yAxis': { 'min': 0, 'max': 100, 'title': { 'text': 'Stakeholder Meeting Input' }},
            'legend': { 'enabled': False },
            'tooltip': { 'pointFormat': 'Usage percentage: <strong>{point.y}%</strong>' },
            'exporting': { 'enabled': False },
            'series': [{
                'name': 'Stakeholder Meeting Input',
                'data': data,
                'color': '#337AB7',
                'dataLabels': {
                    'enabled': True,
                    'color': '#FFFFFF',
                    'align': 'right',
                    'format': '{point.y}%',
                    'style': self.label_style
                }
            }]
        }

        return options

    def factors_usage_bar_chart(self, meeting):
        evaluations = Evaluation.get_evaluations_by_meeting(meeting)
        factors = Factor.list()
        data = []

        meeting_items_count = meeting.meetingitem_set.count()
        stakeholders_count = meeting.meetingstakeholder_set.count()

        max_votes = stakeholders_count * meeting_items_count

        for factor in factors:
            votes = evaluations.filter(factor=factor).exclude(measure_value__description='N/A').count()
            percentage = get_votes_percentage(max_votes, votes)
            if factor.group:
                data.append([u'{0} ({1})'.format(factor.name, factor.group.name), percentage])
            else:
                data.append([factor.name, percentage])

        data = sorted(data, key=operator.itemgetter(1))
        data.reverse()

        options = {
            'chart': { 'type': 'column' },
            'title': { 'text': 'Overall Value Factors Usage' },
            'subtitle': { 'text': 'Which factors are being used to evaluate the decision items.' },
            'xAxis': {
                'type': 'category',
                'labels': { 'style': self.label_style }
            },
            'yAxis': { 'min': 0, 'max': 100, 'title': { 'text': 'Factors usage percentage' }},
            'legend': { 'enabled': False },
            'tooltip': { 'pointFormat': 'Usage percentage: <strong>{point.y}%</strong>' },
            'exporting': { 'enabled': False },
            'series': [{
                'name': 'Factors usage percentage',
                'data': data,
                'color': '#337AB7',
                'dataLabels': {
                    'enabled': True,
                    'rotation': -90,
                    'color': '#FFFFFF',
                    'align': 'right',
                    'format': '{point.y}%',
                    'y': 10,
                    'style': self.label_style
                }
            }]
        }

        return options

    def value_ranking(self, meeting):
        categories = meeting.meetingitem_set.all().values_list('decision_item__name', flat=True).order_by('-value_ranking')
        data = meeting.meetingitem_set.all().values_list('value_ranking', flat=True).order_by('-value_ranking')
        data = [round(value, 2) for value in data]

        options = {
            'chart': { 'type': 'column' },
            'title': { 'text': 'Value Ranking' },
            'exporting': { 'enabled': False },
            'xAxis': { 
                'categories': list(categories)
            },
            'series': [{
                'name': 'Ranking',
                'data': list(data),
                'color': '#337AB7',
                'dataLabels': {
                    'enabled': True
                }
            }]
        }
        return options

    def feature_comparison_bar_chart(self, meeting, measure_value, stakeholder_ids):
        stakeholder_ids = list(set(stakeholder_ids))
        evaluations = Evaluation.get_evaluations_by_meeting(meeting)
        filtered_evaluations = evaluations.filter(measure_value=measure_value, user_id__in=stakeholder_ids)

        stakeholders_count = len(stakeholder_ids)
        factors_count = Factor.list().count()
        max_votes = stakeholders_count * factors_count

        vqs = filtered_evaluations.values('meeting_item__id', 'meeting_item__decision_item__name').annotate(count=Count('meeting_item__id')).order_by('-count')

        data = []
        for result in vqs:
            percentage = get_votes_percentage(max_votes, result['count'])
            data.append([result['meeting_item__decision_item__name'], percentage])

        groups_text = get_stakeholders_group_names(stakeholder_ids)
        options = {
            'chart': { 'type': 'column' },
            'title': { 'text': u'Features Comparison: {0} {1}'.format(measure_value.description, measure_value.measure.name) },
            'subtitle': { 'text': u'{0} opinion'.format(groups_text) },
            'xAxis': {
                'type': 'category',
                'labels': {
                    'rotation': -45,
                    'style': self.label_style
                }
            },
            'yAxis': { 'min': 0, 'title': { 'text': measure_value.description + ' ' + measure_value.measure.name }},
            'legend': { 'enabled': False },
            'tooltip': { 'pointFormat': measure_value.description + ' ' + measure_value.measure.name + ': <strong>{point.y}%</strong>' },
            'exporting': { 'enabled': False },
            'series': [{
                'name': measure_value.description + ' Votes',
                'data': data,
                'color': measure_value.color,
                'dataLabels': {
                    'enabled': True,
                    'rotation': -90,
                    'color': '#FFFFFF',
                    'align': 'right',
                    'format': '{point.y}%',
                    'y': 10,
                    'style': self.label_style
                }
            }]
        }

        return options

    def decision_items_overview(self, meeting, chart, stakeholder_ids):
        stakeholder_ids = list(set(stakeholder_ids))
        evaluations = Evaluation.get_evaluations_by_meeting(meeting).filter(user_id__in=stakeholder_ids)
        options = dict()
        if evaluations.exists():
            measure = meeting.deliverable.measure
            stakeholders_count = len(stakeholder_ids)
            factors_count = Factor.list().count()
            max_votes = stakeholders_count * factors_count

            categories = []
            series = []

            for meeting_item in meeting.meetingitem_set.all():
                categories.append(meeting_item.decision_item.name)

            for measure_value in measure.measurevalue_set.all():
                serie_data = []
                for meeting_item in meeting.meetingitem_set.all():
                    votes = evaluations.filter(measure_value=measure_value, meeting_item=meeting_item).count()
                    percentage = get_votes_percentage(max_votes, votes)
                    serie_data.append(percentage)
                series.append({ 'name': measure_value.description, 'data': serie_data, 'color': measure_value.color })

            options = self._base_stacked_chart(categories, series, chart)
            groups_text = get_stakeholders_group_names(stakeholder_ids)
            options['subtitle'] = { 'text': u'{0} opinion'.format(groups_text) }

        options['title'] = { 'text': u'Decision Items Overview' }
        return options


    ''' Factors Comparison Charts '''

    def _factors_comparison_chart(self, chart_type, evaluations, max_votes):
        options = dict()

        if evaluations:
            evaluations = evaluations.select_related('factor', 'factor__group', 'measure', 'measure_value')
            measure = evaluations[0].measure

            data = {}
            measure_values = measure.measurevalue_set.values_list('description', flat=True)
            for evaluation in evaluations:
                if evaluation.factor.group:
                    label = u'<strong style="text-decoration: underline;">{0}:</strong> {1}'.format(evaluation.factor.group.name, evaluation.factor.name)
                else:
                    label = evaluation.factor.name
                data[label] = {}
                for value in measure_values:
                    data[label][value] = 0

            for evaluation in evaluations:
                if evaluation.factor.group:
                    label = u'<strong style="text-decoration: underline;">{0}:</strong> {1}'.format(evaluation.factor.group.name, evaluation.factor.name)
                else:
                    label = evaluation.factor.name
                data[label][evaluation.measure_value.description] += 1

            sorted_data = sorted(data.items(), key=operator.itemgetter(0))

            categories = []
            for factor in sorted_data:
                categories.append(factor[0])

            series = []
            for value in measure.measurevalue_set.all():
                serie_data = []
                for factor in sorted_data:
                    percentage = get_votes_percentage(max_votes, factor[1][value.description])
                    serie_data.append(percentage)
                series.append({ 'name': value.description, 'data': serie_data, 'color': value.color })

            options = self._base_stacked_chart(categories, series, chart_type)
        
        return options

    def factors_comparison(self, meeting_id, meeting_item_id, chart_type, stakeholder_ids):
        meeting = Meeting.objects.get(pk=meeting_id)
        meeting_item = MeetingItem.objects.get(pk=meeting_item_id)
        evaluations = Evaluation.get_evaluations_by_meeting(meeting).filter(meeting_item=meeting_item, user_id__in=stakeholder_ids)
        max_votes = len(stakeholder_ids)

        options = self._factors_comparison_chart(chart_type, evaluations, max_votes)
        groups_text = get_stakeholders_group_names(stakeholder_ids)
        options['title'] = { 'text': u'{0} Value Factors Comparison'.format(meeting_item.decision_item.name) }
        options['subtitle'] = { 'text': u'{0} opinion'.format(groups_text) }

        return options
    
    def factors_comparison_scenario(self, meeting, scenario, chart_type, stakeholder_ids):
        evaluations = Evaluation.get_evaluations_by_meeting(meeting).filter(meeting_item__in=scenario.meeting_items.all(), user_id__in=stakeholder_ids)
        items_count = scenario.meeting_items.count()
        max_votes = len(stakeholder_ids) * items_count

        options = self._factors_comparison_chart(chart_type, evaluations, max_votes)
        groups_text = get_stakeholders_group_names(stakeholder_ids)
        options['title'] = { 'text': u'{0} Value Factors Comparison'.format(escape(scenario.name)) }
        options['subtitle'] = { 'text': u'{0} opinion'.format(groups_text) }

        return options


    ''' Decision Items Acceptance Charts '''

    ''' Simple Treemap '''

    def _decision_item_acceptance_simple_treemap(self, evaluations):
        vqs = evaluations.values('measure_value__description', 'measure_value__color').annotate(value=Count('measure_value__description')).order_by()
        data = [kv for kv in vqs]
        for d in data:
            d['name'] = d.pop('measure_value__description')
            d['color'] = d.pop('measure_value__color')
        options = self._base_treemap(data)
        return options

    def decision_item_acceptance_simple_treemap(self, meeting_item, stakeholder_ids):
        evaluations = Evaluation.get_evaluations_by_meeting(meeting_item.meeting).filter(meeting_item=meeting_item, user_id__in=stakeholder_ids)
        options = self._decision_item_acceptance_simple_treemap(evaluations)
        groups_text = get_stakeholders_group_names(stakeholder_ids)
        options['title'] = { 'text': u'{0} Acceptance'.format(escape(meeting_item.decision_item.name)) }
        options['subtitle'] = { 'text': u'{0} opinion'.format(groups_text) }
        return options

    def decision_item_acceptance_scenario_simple_treemap(self, scenario, stakeholder_ids):
        evaluations = Evaluation.get_evaluations_by_meeting(scenario.meeting) \
                .filter(meeting_item__in=scenario.meeting_items.all(), user_id__in=stakeholder_ids)
        options = self._decision_item_acceptance_simple_treemap(evaluations)
        groups_text = get_stakeholders_group_names(stakeholder_ids)
        options['title'] = { 'text': u'{0} Acceptance'.format(escape(scenario.name)) }
        options['subtitle'] = { 'text': u'{0} opinion'.format(groups_text) }
        return options

    ''' Detailed Treemap '''

    def _decision_item_acceptance_detailed_treemap(self, evaluations):
        vqs = evaluations.order_by('measure_value__description', 'measure_value__id', 'measure_value__color') \
            .distinct('measure_value__description', 'measure_value__id', 'measure_value__color') \
            .values('measure_value__description', 'measure_value__id', 'measure_value__color')
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
        options = self._base_treemap(data)

        return options

    def decision_item_acceptance_detailed_treemap(self, meeting_item, stakeholder_ids):
        evaluations = Evaluation.get_evaluations_by_meeting(meeting_item.meeting).filter(meeting_item=meeting_item, user_id__in=stakeholder_ids)
        options = self._decision_item_acceptance_detailed_treemap(evaluations)
        options['title'] = { 'text': u'{0} Acceptance'.format(escape(meeting_item.decision_item.name)) }
        groups_text = get_stakeholders_group_names(stakeholder_ids)
        options['subtitle'] = { 'text': u'{0} opinion'.format(groups_text) }
        return options

    def decision_item_acceptance_scenario_detailed_treemap(self, scenario, stakeholder_ids):
        evaluations = Evaluation.get_evaluations_by_meeting(scenario.meeting) \
            .filter(meeting_item__in=scenario.meeting_items.all(), user_id__in=stakeholder_ids)
        options = self._decision_item_acceptance_detailed_treemap(evaluations)
        options['title'] = { 'text': u'{0} Acceptance'.format(escape(scenario.name)) }
        groups_text = get_stakeholders_group_names(stakeholder_ids)
        options['subtitle'] = { 'text': u'{0} opinion'.format(groups_text) }
        return options

    ''' Pie Chart Drilldown '''

    def _decision_item_acceptance_pie_chart_drilldown(self, evaluations):
        vqs = evaluations.values('measure_value__description', 'measure_value__color').annotate(y=Count('measure_value__description')).order_by('y')
        series = [kv for kv in vqs]
        for serie in series:
            serie['name'] = serie['measure_value__description']
            serie['drilldown'] = serie['measure_value__description']
            del serie['measure_value__description']
            serie['color'] = serie.pop('measure_value__color')

        vqs = evaluations.order_by('measure_value__id', 'measure_value__description').distinct('measure_value__id', 'measure_value__description').values('measure_value__id', 'measure_value__description')
        drilldown_series = []
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
            drilldown_series.append(drilldown)
        
        options = {
            'chart': { 'type': 'pie' },
            'plotOptions': { 'series': { 'dataLabels': { 'enabled': True, 'format': '{point.name}: {point.y} votes' } } },
            'exporting': { 'enabled': False },
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
                'series': drilldown_series
            }
        }
        return options

    def decision_item_acceptance_pie_chart_drilldown(self, meeting_item, stakeholder_ids):
        evaluations = Evaluation.get_evaluations_by_meeting(meeting_item.meeting).filter(meeting_item=meeting_item, user_id__in=stakeholder_ids)
        options = self._decision_item_acceptance_pie_chart_drilldown(evaluations)
        groups_text = get_stakeholders_group_names(stakeholder_ids)
        options['title'] = { 'text': u'{0} Acceptance'.format(escape(meeting_item.decision_item.name)) }
        options['subtitle'] = { 'text': u'{0} opinion. Click the slices to view value factors.'.format(groups_text) }
        return options

    def decision_item_acceptance_scenario_pie_chart_drilldown(self, scenario, stakeholder_ids):
        evaluations = Evaluation.get_evaluations_by_meeting(scenario.meeting) \
            .filter(meeting_item__in=scenario.meeting_items.all(), user_id__in=stakeholder_ids)
        options = self._decision_item_acceptance_pie_chart_drilldown(evaluations)
        groups_text = get_stakeholders_group_names(stakeholder_ids)
        options['title'] = { 'text': u'{0} Acceptance'.format(escape(scenario.name)) }
        options['subtitle'] = { 'text': u'{0} opinion. Click the slices to view value factors.'.format(groups_text) }
        return options

    ''' Factors Groups Comparison '''

    def _factors_groups(self, evaluations, stakeholder_ids, aggregated_max_votes=1):
        categories = evaluations.values_list('factor__group__name', flat=True).distinct().order_by('factor__group__name')
        options = dict()
        if evaluations.exists():
            measure = evaluations.first().measure
            series = []
            for measure_value in measure.measurevalue_set.all():
                serie = { 
                        'name': measure_value.description, 
                        'color': measure_value.color, 
                        'pointPlacement': 'on', 
                        'data': list()
                    }
                for category in categories:
                    group = FactorGroup.objects.get(name=category)
                    factors_count = group.factor_set.count()
                    max_votes = factors_count * len(stakeholder_ids) * aggregated_max_votes
                    votes = evaluations.filter(factor__group__name=category, measure_value=measure_value).count()
                    percentage = get_votes_percentage(max_votes, votes)
                    serie['data'].append(percentage)
                series.append(serie)

            categories = [category if category else 'No group' for category in categories]

            options = {
                'chart': { 'polar': True, 'type': 'line' },
                'xAxis': {
                    'categories': list(categories),
                    'tickmarkPlacement': 'on',
                    'lineWidth': 0
                },
                'yAxis': {
                    'gridLineInterpolation': 'polygon',
                    'min': 0,
                    'max': 100,
                    'labels': { 'format': '{value}%' }
                },
                'tooltip': {
                    'shared': True,
                    'pointFormat': '<span style="color:{series.color}">{series.name}: <b>{point.y} votes</b><br/>'
                },
                'exporting': { 'enabled': False },
                'series': series
            }
        return options


    def factors_groups(self, meeting_item, stakeholder_ids):
        evaluations = Evaluation.get_evaluations_by_meeting(meeting_item.meeting) \
                .filter(meeting_item=meeting_item, user_id__in=stakeholder_ids)
        options = self._factors_groups(evaluations, stakeholder_ids)
        stakeholders_text = get_stakeholders_group_names(stakeholder_ids)
        subtitle = '<strong>Stakeholders Roles:</strong> {0}'.format(stakeholders_text)
        options['title'] = { 'text': escape(meeting_item.decision_item.name) }
        options['subtitle'] = { 'text': subtitle }
        return options

    def factors_groups_scenario(self, meeting, scenario, stakeholder_ids):
        evaluations = Evaluation.get_evaluations_by_meeting(meeting) \
                .filter(meeting_item__in=scenario.meeting_items.all(), user_id__in=stakeholder_ids)
        aggregated_max_votes = scenario.meeting_items.count()
        options = self._factors_groups(evaluations, stakeholder_ids, aggregated_max_votes)
        items_names = scenario.meeting_items.values_list('decision_item__name', flat=True)
        items_text = u', '.join(items_names)
        stakeholders_text = get_stakeholders_group_names(stakeholder_ids)
        subtitle = u'<strong>Decision Items:</strong> {0}<br><strong>Stakeholders Roles:</strong> {1}'.format(escape(items_text), stakeholders_text)
        options['title'] = { 'text': escape(scenario.name) }
        options['subtitle'] = { 'text': subtitle }
        return options
