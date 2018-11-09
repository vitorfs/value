# coding: utf-8
import math
import operator

from django.contrib.auth.models import User
from django.db.models import Count
from django.utils.html import escape
from django.utils.translation import ugettext as _

from value.factors.models import Group as FactorGroup
from value.deliverables.meetings.models import Meeting, MeetingItem, Evaluation
from value.deliverables.meetings.utils import get_votes_percentage


def get_stakeholders_group_names(stakeholder_ids):
    stakeholders = User.objects.filter(id__in=stakeholder_ids) \
        .prefetch_related('groups')
    groups = set()
    for stakeholder in stakeholders:
        for group in stakeholder.groups.all():
            groups.add(group.name)
    groups_text = u', '.join(groups)
    return escape(groups_text)


class Highcharts(object):

    def __init__(self):
        self.label_style = {'fontSize': '13px', 'fontFamily': '"Helvetica Neue", Helvetica, Arial, sans-serif'}

    ''' Support Functions '''

    def _base_stacked_chart(self, categories, series, chart='stacked_columns'):
        chart_type = 'bar'
        stacking = None

        if chart in ['stacked_bars', 'stacked_columns', 'balanced_columns']:
            stacking = 'normal'

        if chart in ['stacked_columns', 'basic_columns']:
            chart_type = 'column'

        options = {
            'chart': {'type': chart_type},
            'title': {'text': ''},
            'xAxis': {'categories': categories},
            'yAxis': {
                'min': 0,
                'max': 100,
                'title': {'text': _('Percentage of evaluations')},
                'labels': {'format': '{value}%'}
            },
            'legend': {'reversed': True},
            'plotOptions': {'series': {'stacking': stacking}},
            'tooltip': {'pointFormat': _('Percentage:') + ' <strong>{point.y}%</strong>'},
            'exporting': {'enabled': False},
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
                        'style': {'fontSize': '15px', 'fontWeight': 'bold'}
                    }
                }],
                'data': data,
                'tooltip': {'pointFormat': '{point.name} ' + _('Percentage:') + ' <strong>{point.value}%</strong>'}
            }],
            'exporting': {'enabled': False}
        }
        return options

    def fix_serie_data_percentage(self, series):
        if series:
            size = len(series[0]['data'])
            na_serie = list()
            for i in range(0, size):
                na_serie.append(100.0)
            for serie in series:
                for index, value in enumerate(serie['data']):
                    na_serie[index] -= value
            na_serie = map(lambda x: round(x, 2), na_serie)
            display_serie = reduce(lambda x, y: x + y, na_serie)
            if display_serie > 0:
                series.insert(0, {
                    'name': 'N/A',
                    'data': na_serie,
                    'color': '#cccccc'
                })
        return series

    ''' Summary Charts '''

    def stakeholders_input_bar_chart(self, meeting):
        evaluations = Evaluation.get_evaluations_by_meeting(meeting)
        meeting_stakeholders = meeting.meetingstakeholder_set.all()
        factors = meeting.factors.all()

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
            'chart': {'type': 'bar'},
            'title': {'text': _('Stakeholders Input')},
            'subtitle': {'text': _('100% means the stakeholder evaluated all the meeting\'s decision items.')},
            'xAxis': {
                'type': 'category',
                'labels': {'style': self.label_style}
            },
            'yAxis': {'min': 0, 'max': 100, 'title': {'text': _('Stakeholder Meeting Input')}},
            'legend': {'enabled': False},
            'tooltip': {'pointFormat': _('Usage percentage:') + ' <strong>{point.y}%</strong>'},
            'exporting': {'enabled': False},
            'series': [{
                'name': _('Stakeholder Meeting Input'),
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
        factors = meeting.factors.all()
        data = list()

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
            'chart': {'type': 'column'},
            'title': {'text': _('Overall Value Factors Usage')},
            'subtitle': {'text': _('Which factors are being used to evaluate the decision items.')},
            'xAxis': {
                'type': 'category',
                'labels': {'style': self.label_style}
            },
            'yAxis': {'min': 0, 'max': 100, 'title': {'text': _('Factors usage percentage')}},
            'legend': {'enabled': False},
            'tooltip': {'pointFormat': _('Usage percentage:') + ' <strong>{point.y}%</strong>'},
            'exporting': {'enabled': False},
            'series': [{
                'name': _('Factors usage percentage'),
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

    def _value_ranking(self, meeting_items):
        categories = meeting_items.values_list('decision_item__name', flat=True).order_by('-value_ranking')
        data = meeting_items.values_list('value_ranking', flat=True).order_by('-value_ranking')
        data = [round(value, 2) for value in data]

        options = {
            'chart': {'type': 'column'},
            'title': {'text': _('Value Ranking')},
            'exporting': {'enabled': False},
            'xAxis': {
                'categories': list(categories)
            },
            'series': [{
                'name': _('Ranking'),
                'data': list(data),
                'color': '#337AB7',
                'dataLabels': {
                    'enabled': True
                }
            }]
        }
        return options

    def value_ranking(self, meeting):
        meeting_items = meeting.meetingitem_set.all()
        return self._value_ranking(meeting_items)

    def value_ranking_scenario(self, scenario):
        meeting_items = scenario.meeting_items.all()
        return self._value_ranking(meeting_items)

    def feature_comparison_bar_chart(self, meeting, measure_value, stakeholder_ids):
        stakeholder_ids = list(set(stakeholder_ids))
        evaluations = Evaluation.get_evaluations_by_meeting(meeting)
        filtered_evaluations = evaluations.filter(measure_value=measure_value, user_id__in=stakeholder_ids)

        stakeholders_count = len(stakeholder_ids)
        factors_count = meeting.factors.count()
        max_votes = stakeholders_count * factors_count

        vqs = filtered_evaluations \
            .values('meeting_item__id', 'meeting_item__decision_item__name') \
            .annotate(count=Count('meeting_item__id')) \
            .order_by('-count')

        data = []
        for result in vqs:
            percentage = get_votes_percentage(max_votes, result['count'])
            data.append([result['meeting_item__decision_item__name'], percentage])

        groups_text = get_stakeholders_group_names(stakeholder_ids)
        options = {
            'chart': {'type': 'column'},
            'title': {'text': u'{0}: {1} {2}'.format(
                _('Features Comparison'),
                measure_value.description,
                measure_value.measure.name
            )},
            'subtitle': {'text': u'{0} opinion'.format(groups_text)},
            'xAxis': {
                'type': 'category',
                'labels': {
                    'rotation': -45,
                    'style': self.label_style
                }
            },
            'yAxis': {'min': 0, 'title': {'text': measure_value.description + ' ' + measure_value.measure.name}},
            'legend': {'enabled': False},
            'tooltip': {
                'pointFormat': u'{0} {1}:'.format(
                    measure_value.description,
                    measure_value.measure.name
                ) + '<strong>{point.y}%</strong>'
            },
            'exporting': {'enabled': False},
            'series': [{
                'name': measure_value.description + ' ' + _('Votes'),
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

    def _build_evaluation_grid(self, meeting, evaluations, meeting_items):
        '''
        Resulting list:
        [
            [336, u'Feature 1', -5.55, 9, 11, 11, 14, 9],
            [337, u'Feature 2', 7.40, 10, 11, 16, 9, 8],
            ...
        ]
        id, decision_item_name, value_ranking, measure_value_1, measure_value_2, ..., measure_value_n
        '''
        evaluation_list = evaluations.select_related('measure_value', 'meeting_item') \
            .values('meeting_item', 'measure_value') \
            .annotate(votes=Count('measure_value')) \
            .order_by('meeting_item', 'measure_value__order')
        evaluation_grid = list()

        measure_values = meeting.measure.measurevalue_set.all()
        measure_value_count = measure_values.count()
        for meeting_item in meeting_items:
            meeting_item_data = [
                meeting_item.pk,
                meeting_item.decision_item.name,
                meeting_item.value_ranking,
            ] + map(lambda x: 0, range(measure_value_count))

            for index, measure_value in enumerate(measure_values):
                for evaluation in evaluation_list:
                    if evaluation['meeting_item'] == meeting_item.pk and evaluation['measure_value'] == measure_value.pk:
                        meeting_item_data[index + 3] = evaluation['votes']
            evaluation_grid.append(meeting_item_data)

        return evaluation_grid

    def _decision_items_overview(self, meeting, chart_type, stakeholder_ids, evaluations, meeting_items):
        options = dict()
        if evaluations.exists():
            ID = 0
            NAME = 1
            VALUE_RANKING = 2
            OFFSET = len((ID, NAME, VALUE_RANKING, ))

            measure = meeting.measure
            stakeholders_count = len(stakeholder_ids)
            factors_count = meeting.factors.count()
            max_votes = stakeholders_count * factors_count

            evaluation_grid = self._build_evaluation_grid(meeting, evaluations, meeting_items)
            evaluation_grid.sort(key=lambda x: (-x[2], -x[3]))

            categories = map(lambda item: item[NAME], evaluation_grid)
            series = list()

            for index, measure_value in enumerate(measure.measurevalue_set.all()):
                series.append({
                    'name': measure_value.description,
                    'data': map(lambda item: get_votes_percentage(max_votes, item[index + OFFSET]), evaluation_grid),
                    'color': measure_value.color
                })

            series = self.fix_serie_data_percentage(series)
            options = self._base_stacked_chart(categories, series, chart_type)
            groups_text = get_stakeholders_group_names(stakeholder_ids)
            options['subtitle'] = {'text': u'{0} {1}'.format(groups_text, _('opinion'))}
        return options

    def _balanced_decision_items_overview(self, meeting, stakeholder_ids, evaluations, meeting_items):
        options = dict()
        if evaluations.exists():
            ID = 0
            NAME = 1
            VALUE_RANKING = 2
            OFFSET = len((ID, NAME, VALUE_RANKING, ))

            measure = meeting.measure
            evaluation_grid = self._build_evaluation_grid(meeting, evaluations, meeting_items)
            evaluation_grid.sort(key=lambda x: (-x[2], -x[3]))
            categories = map(lambda item: item[NAME], evaluation_grid)
            series = list()

            for index, measure_value in enumerate(measure.measurevalue_set.all()):
                series.append({
                    'type': 'column',
                    'stacking': 'normal',
                    'yAxis': 0,
                    'tooltip': {'valueSuffix': '%'},
                    'name': measure_value.description,
                    'data': map(lambda item: get_votes_percentage(sum(item[3:]), item[index + OFFSET]), evaluation_grid),
                    'color': measure_value.color
                })

            stakeholders_data = list()
            for item in evaluation_grid:
                stakeholders_count = evaluations.filter(meeting_item=item[ID]) \
                    .values('user') \
                    .order_by('user') \
                    .distinct() \
                    .count()
                stakeholders_data.append(stakeholders_count)

            series.append({
                'name': _('Stakeholders'),
                'type': 'line',
                'yAxis': 1,
                'data': stakeholders_data,
                # 'color': '#fe0074'
                'color': 'transparent',
                'dataLabels': {
                    'enabled': True
                }
            })

            options = {
                'chart': {
                    'zoomType': 'xy'
                },
                'xAxis': [{
                    'categories': categories,
                    'crosshair': True
                }],
                'yAxis': [
                    {
                        'title': {'text': _('Percentage of evaluations')},
                        'labels': {'format': '{value}%'},
                        'floor': 0,
                        'ceiling': 100
                    },
                    {
                        'title': {'text': _('Number of Stakeholders')},
                        'labels': {'format': '{value}',},
                        'opposite': True,
                        'color': '#fe0074'
                    }
                ],
                'tooltip': {
                    'shared': True
                },
                'series': series
            }

            groups_text = get_stakeholders_group_names(stakeholder_ids)
            options['subtitle'] = {'text': u'{0} {1}'.format(groups_text, _('opinion'))}
        return options

    def decision_items_overview(self, meeting, chart_type, stakeholder_ids):
        stakeholder_ids = list(set(stakeholder_ids))
        evaluations = Evaluation.get_evaluations_by_meeting(meeting).filter(user_id__in=stakeholder_ids)
        meeting_items = meeting.meetingitem_set.select_related('decision_item').all()

        if chart_type == 'balanced_columns':
            options = self._balanced_decision_items_overview(meeting, stakeholder_ids, evaluations, meeting_items)
        else:
            options = self._decision_items_overview(meeting, chart_type, stakeholder_ids, evaluations, meeting_items)

        options['title'] = {'text': _(u'Decision Items Overview')}
        return options

    def decision_items_overview_scenario(self, scenario, chart_type, stakeholder_ids):
        stakeholder_ids = list(set(stakeholder_ids))
        evaluations = Evaluation.get_evaluations_by_meeting(scenario.meeting)\
            .filter(user_id__in=stakeholder_ids, meeting_item__in=scenario.meeting_items.all())
        meeting_items = scenario.meeting_items.all()

        if chart_type == 'balanced_columns':
            options = self._balanced_decision_items_overview(scenario.meeting, stakeholder_ids,
                                                             evaluations, meeting_items)
        else:
            options = self._decision_items_overview(scenario.meeting, chart_type, stakeholder_ids,
                                                    evaluations, meeting_items)
        options['title'] = {'text': _(u'Scenario Overview')}
        return options

    ''' Factors Comparison Charts '''

    def _factors_comparison_chart(self, chart_type, evaluations, max_votes):
        options = dict()

        if evaluations:
            evaluations = evaluations.select_related('factor', 'factor__group', 'measure', 'measure_value')
            measure = evaluations.first().measure

            data = dict()
            measure_values = measure.measurevalue_set.values_list('description', flat=True)
            for evaluation in evaluations:
                if evaluation.factor.group:
                    label = u'<strong style="text-decoration: underline;">{0}:</strong> {1}'.format(
                        evaluation.factor.group.name,
                        evaluation.factor.name
                    )
                else:
                    label = evaluation.factor.name
                data[label] = dict()
                for value in measure_values:
                    data[label][value] = 0

            for evaluation in evaluations:
                if evaluation.factor.group:
                    label = u'<strong style="text-decoration: underline;">{0}:</strong> {1}'.format(
                        evaluation.factor.group.name,
                        evaluation.factor.name
                    )
                else:
                    label = evaluation.factor.name
                data[label][evaluation.measure_value.description] += 1

            sorted_data = sorted(data.items(), key=operator.itemgetter(0))

            categories = list()
            for factor in sorted_data:
                categories.append(factor[0])

            series = list()
            for value in measure.measurevalue_set.all():
                serie_data = list()
                for factor in sorted_data:
                    percentage = get_votes_percentage(max_votes, factor[1][value.description])
                    serie_data.append(percentage)
                series.append({'name': value.description, 'data': serie_data, 'color': value.color})

            series = self.fix_serie_data_percentage(series)

            options = self._base_stacked_chart(categories, series, chart_type)

        return options

    def _balanced_factors_comparison_chart(self, evaluations):
        options = dict()
        if evaluations:
            data = dict()
            evaluations = evaluations.select_related('factor', 'factor__group', 'measure', 'measure_value')
            measure = evaluations.first().measure
            measure_values = measure.measurevalue_set.values_list('description', flat=True)

            for evaluation in evaluations:
                if evaluation.factor.group:
                    label = u'<strong style="text-decoration: underline;">{0}:</strong> {1}'.format(
                        evaluation.factor.group.name,
                        evaluation.factor.name
                    )
                else:
                    label = evaluation.factor.name
                data[label] = dict()
                for value in measure_values:
                    data[label][value] = 0

            for evaluation in evaluations:
                if evaluation.factor.group:
                    label = u'<strong style="text-decoration: underline;">{0}:</strong> {1}'.format(
                        evaluation.factor.group.name,
                        evaluation.factor.name
                    )
                else:
                    label = evaluation.factor.name
                data[label][evaluation.measure_value.description] += 1

            sorted_data = sorted(data.items(), key=operator.itemgetter(0))

            categories = list()
            for factor in sorted_data:
                categories.append(factor[0])

            series = list()
            for value in measure.measurevalue_set.all():
                serie_data = list()
                for factor in sorted_data:
                    max_votes = 0
                    for measurekey, count in factor[1].iteritems():
                        max_votes += count
                    percentage = int(round(get_votes_percentage(max_votes, factor[1][value.description])))
                    serie_data.append(percentage)
                series.append({'name': value.description, 'data': serie_data, 'color': value.color})

            # fix the percentage overflow (e.g. sum = 100.01)
            for index, factor in enumerate(sorted_data):
                _max_value = 0
                _max_index = 0
                _factor_total = 0
                for serie_index, serie in enumerate(series):
                    _value = serie['data'][index]
                    _factor_total += _value
                    if _value >= _max_value:
                        _max_value = _value
                        _max_index = serie_index
                if _factor_total > 100:
                    _rest = _factor_total - 100
                    series[_max_index]['data'][index] = int(round(_max_value - _rest))


            for index, factor in enumerate(sorted_data):
                _factor_total = 0
                for serie_index, serie in enumerate(series):
                    _value = serie['data'][index]
                    _factor_total += _value
                print _factor_total
                print type(_factor_total)

            stakeholders_data = list()
            for factor in sorted_data:
                stakeholders_count = 0
                for measurekey, count in factor[1].iteritems():
                    stakeholders_count += count
                stakeholders_data.append(stakeholders_count)

            for index, serie in enumerate(series):
                series[index].update({
                    'type': 'column',
                    'stacking': 'normal',
                    'yAxis': 0,
                    'tooltip': {'valueSuffix': '%'}
                })

            series.append({
                'name': 'Stakeholders',
                'type': 'line',
                'yAxis': 1,
                'data': stakeholders_data,
                'color': 'transparent',
                'dataLabels': {
                    'enabled': True
                }
            })

            options = {
                'chart': {
                    'type': 'column',
                    'zoomType': 'xy'
                },
                'xAxis': [{
                    'categories': categories,
                    'crosshair': True
                }],
                'yAxis': [
                    {
                        'title': {'text': _('Percentage of evaluations')},
                        'labels': {'format': '{value}%'},
                        'max': 100,
                        'min': 0
                    },
                    {
                    'title': {
                        'text': _('Number of Stakeholders')
                    },
                    'labels': {
                        'format': '{value}',
                    },
                    'opposite': True
                }],
                'tooltip': {
                    'shared': True
                },
                'series': series
            }

        return options

    def factors_comparison(self, meeting_id, meeting_item_id, chart_type, stakeholder_ids):
        meeting = Meeting.objects.get(pk=meeting_id)
        meeting_item = MeetingItem.objects.get(pk=meeting_item_id)
        evaluations = Evaluation.get_evaluations_by_meeting(meeting) \
            .filter(meeting_item=meeting_item, user_id__in=stakeholder_ids)

        if chart_type == 'balanced_columns':
            options = self._balanced_factors_comparison_chart(evaluations)
        else:
            max_votes = len(set(stakeholder_ids))
            options = self._factors_comparison_chart(chart_type, evaluations, max_votes)

        groups_text = get_stakeholders_group_names(stakeholder_ids)
        options['title'] = {'text': u'{0} {1}'.format(
            meeting_item.decision_item.name, _('Value Factors Comparison')
        )}
        options['subtitle'] = {'text': u'{0} {1}'.format(groups_text, _('opinion'))}
        return options

    def factors_comparison_scenario(self, meeting, scenario, chart_type, stakeholder_ids):
        evaluations = Evaluation.get_evaluations_by_meeting(meeting) \
            .filter(meeting_item__in=scenario.meeting_items.all(), user_id__in=stakeholder_ids)
        items_count = scenario.meeting_items.count()

        if chart_type == 'balanced_columns':
            options = self._balanced_factors_comparison_chart(evaluations)
        else:
            max_votes = len(stakeholder_ids) * items_count
            options = self._factors_comparison_chart(chart_type, evaluations, max_votes)

        groups_text = get_stakeholders_group_names(stakeholder_ids)
        options['title'] = {'text': u'{0} {1}'.format(
            escape(scenario.name), _('Value Factors Comparison')
        )}
        options['subtitle'] = {'text': u'{0} {1}'.format(groups_text, _('opinion'))}
        return options

    ''' Decision Items Acceptance Charts '''

    ''' Simple Treemap '''

    def _decision_item_acceptance_simple_treemap(self, evaluations, max_votes):
        options = dict()
        if evaluations.exists():
            vqs = evaluations \
                .values('measure_value__description', 'measure_value__color') \
                .annotate(value=Count('measure_value__description')) \
                .order_by()
            data = [kv for kv in vqs]
            for d in data:
                d['name'] = d.pop('measure_value__description')
                d['color'] = d.pop('measure_value__color')
                d['value'] = get_votes_percentage(max_votes, d.pop('value'))
            options = self._base_treemap(data)
        return options

    def decision_item_acceptance_simple_treemap(self, meeting_item, stakeholder_ids):
        evaluations = Evaluation \
            .get_evaluations_by_meeting(meeting_item.meeting) \
            .filter(meeting_item=meeting_item, user_id__in=stakeholder_ids)
        factors_count = meeting_item.meeting.factors.count()
        max_votes = factors_count * len(stakeholder_ids)

        options = self._decision_item_acceptance_simple_treemap(evaluations, max_votes)
        groups_text = get_stakeholders_group_names(stakeholder_ids)
        options['title'] = {'text': u'{0} {1}'.format(
            escape(meeting_item.decision_item.name), _('Acceptance')
        )}
        options['subtitle'] = {'text': u'{0} {1}'.format(groups_text, _('opinion'))}
        return options

    def decision_item_acceptance_scenario_simple_treemap(self, scenario, stakeholder_ids):
        evaluations = Evaluation.get_evaluations_by_meeting(scenario.meeting) \
            .filter(meeting_item__in=scenario.meeting_items.all(), user_id__in=stakeholder_ids)
        factors_count = scenario.meeting.factors.count()
        meeting_items_count = scenario.meeting_items.count()
        max_votes = factors_count * len(stakeholder_ids) * meeting_items_count

        options = self._decision_item_acceptance_simple_treemap(evaluations, max_votes)
        groups_text = get_stakeholders_group_names(stakeholder_ids)
        options['title'] = {'text': u'{0} {1}'.format(
            escape(scenario.name), _('Acceptance')
        )}
        options['subtitle'] = {'text': u'{0} {1}'.format(groups_text, _('opinion'))}
        return options

    ''' Detailed Treemap '''

    def _decision_item_acceptance_detailed_treemap(self, evaluations, max_votes):
        vqs = evaluations.order_by('measure_value__description', 'measure_value__id', 'measure_value__color') \
            .distinct('measure_value__description', 'measure_value__id', 'measure_value__color') \
            .values('measure_value__description', 'measure_value__id', 'measure_value__color')
        groups = [kv for kv in vqs]
        for g in groups:
            g['id'] = g['measure_value__description']
            g['name'] = g['measure_value__description']
            del g['measure_value__description']
            g['color'] = g.pop('measure_value__color')

        vqs = evaluations \
            .values('measure_value__description', 'factor__name') \
            .annotate(value=Count('measure_value__description')) \
            .order_by()
        data = [kv for kv in vqs]
        for d in data:
            d['name'] = d.pop('factor__name')
            d['parent'] = d.pop('measure_value__description')
            d['value'] = get_votes_percentage(max_votes, d.pop('value'))

        data = groups + data
        options = self._base_treemap(data)

        return options

    def decision_item_acceptance_detailed_treemap(self, meeting_item, stakeholder_ids):
        evaluations = Evaluation.get_evaluations_by_meeting(meeting_item.meeting) \
            .filter(meeting_item=meeting_item, user_id__in=stakeholder_ids)
        factors_count = meeting_item.meeting.factors.count()
        max_votes = factors_count * len(stakeholder_ids)

        options = self._decision_item_acceptance_detailed_treemap(evaluations, max_votes)
        options['title'] = {'text': u'{0} {1}'.format(
            escape(meeting_item.decision_item.name), _('Acceptance')
        )}
        groups_text = get_stakeholders_group_names(stakeholder_ids)
        options['subtitle'] = {'text': u'{0} {1}'.format(groups_text, _('opinion'))}
        return options

    def decision_item_acceptance_scenario_detailed_treemap(self, scenario, stakeholder_ids):
        evaluations = Evaluation.get_evaluations_by_meeting(scenario.meeting) \
            .filter(meeting_item__in=scenario.meeting_items.all(), user_id__in=stakeholder_ids)
        factors_count = scenario.meeting.factors.count()
        meeting_items_count = scenario.meeting_items.count()
        max_votes = factors_count * len(stakeholder_ids) * meeting_items_count

        options = self._decision_item_acceptance_detailed_treemap(evaluations, max_votes)
        options['title'] = {'text': u'{0} {1}'.format(
            escape(scenario.name), _('Acceptance')
        )}
        groups_text = get_stakeholders_group_names(stakeholder_ids)
        options['subtitle'] = {'text': u'{0} {1}'.format(groups_text, _('opinion'))}
        return options

    ''' Pie Chart Drilldown '''

    def _decision_item_acceptance_pie_chart_drilldown(self, evaluations, max_votes):
        vqs = evaluations.values('measure_value__description', 'measure_value__color') \
            .annotate(y=Count('measure_value__description')) \
            .order_by('y')
        series = [kv for kv in vqs]
        for serie in series:
            serie['name'] = serie['measure_value__description']
            serie['drilldown'] = serie['measure_value__description']
            del serie['measure_value__description']
            serie['color'] = serie.pop('measure_value__color')
            serie['y'] = get_votes_percentage(max_votes, serie.pop('y'))

        vqs = evaluations.order_by('measure_value__id', 'measure_value__description') \
            .distinct('measure_value__id', 'measure_value__description') \
            .values('measure_value__id', 'measure_value__description')
        drilldown_series = []
        for v in vqs:
            vqs = evaluations.filter(measure_value__id=v['measure_value__id']) \
                .values('measure_value__description', 'factor__name') \
                .annotate(y=Count('measure_value__description')) \
                .order_by('y')
            data = []
            for value in vqs:
                data.append([value['factor__name'], get_votes_percentage(max_votes, value['y'])])
            drilldown = {
                'data': data,
                'id': v['measure_value__description'],
                'name': v['measure_value__description']
            }
            drilldown_series.append(drilldown)

        options = {
            'chart': {'type': 'pie'},
            'plotOptions': {'series': {'dataLabels': {'enabled': True, 'format': '{point.name}: {point.y}%'}}},
            'exporting': {'enabled': False},
            'tooltip': {
                'headerFormat': '<span style="font-size:11px">{series.name}</span><br>',
                'pointFormat': '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}%</b><br/>'
            },
            'series': [{
                'name': _('Acceptance Summary'),
                'colorByPoint': True,
                'data': series
            }],
            'drilldown': {
                'series': drilldown_series
            }
        }
        return options

    def decision_item_acceptance_pie_chart_drilldown(self, meeting_item, stakeholder_ids):
        evaluations = Evaluation.get_evaluations_by_meeting(meeting_item.meeting) \
            .filter(meeting_item=meeting_item, user_id__in=stakeholder_ids)
        factors_count = meeting_item.meeting.factors.count()
        max_votes = factors_count * len(stakeholder_ids)

        options = self._decision_item_acceptance_pie_chart_drilldown(evaluations, max_votes)
        groups_text = get_stakeholders_group_names(stakeholder_ids)
        options['title'] = {'text': u'{0} {1}'.format(
            escape(meeting_item.decision_item.name), _('Acceptance')
        )}
        options['subtitle'] = {'text': u'{0} {1}. {2}.'.format(
            groups_text, _('opinion'), _('Click the slices to view value factors')
        )}
        return options

    def decision_item_acceptance_scenario_pie_chart_drilldown(self, scenario, stakeholder_ids):
        evaluations = Evaluation.get_evaluations_by_meeting(scenario.meeting) \
            .filter(meeting_item__in=scenario.meeting_items.all(), user_id__in=stakeholder_ids)
        factors_count = scenario.meeting.factors.count()
        meeting_items_count = scenario.meeting_items.count()
        max_votes = factors_count * len(stakeholder_ids) * meeting_items_count

        options = self._decision_item_acceptance_pie_chart_drilldown(evaluations, max_votes)
        groups_text = get_stakeholders_group_names(stakeholder_ids)
        options['title'] = {'text': u'{0} {1}'.format(escape(scenario.name), _('Acceptance'))}
        options['subtitle'] = {'text': u'{0} {1}. {2}.'.format(
            groups_text, _('opinion'), _('Click the slices to view value factors')
        )}
        return options

    ''' Factors Groups Comparison '''

    def _factors_groups(self, evaluations, stakeholder_ids, aggregated_max_votes=1):
        categories = evaluations.values_list('factor__group__name', flat=True) \
            .distinct() \
            .order_by('factor__group__name')
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

            categories = [category if category else _('No group') for category in categories]

            options = {
                'chart': {'polar': True, 'type': 'line'},
                'xAxis': {
                    'categories': list(categories),
                    'tickmarkPlacement': 'on',
                    'lineWidth': 0
                },
                'yAxis': {
                    'gridLineInterpolation': 'polygon',
                    'min': 0,
                    'max': 100,
                    'labels': {'format': '{value}%'}
                },
                'tooltip': {
                    'shared': True,
                    'pointFormat': '<span style="color:{series.color}">{series.name}: <b>{point.y}%</b><br/>',
                },
                'exporting': {'enabled': False},
                'series': series
            }
        return options

    def factors_groups(self, meeting_item, stakeholder_ids):
        evaluations = Evaluation.get_evaluations_by_meeting(meeting_item.meeting) \
            .filter(meeting_item=meeting_item, user_id__in=stakeholder_ids)
        options = self._factors_groups(evaluations, stakeholder_ids)
        stakeholders_text = get_stakeholders_group_names(stakeholder_ids)
        subtitle = u'<strong>{0}:</strong> {1}'.format(_('Stakeholders Roles'), stakeholders_text)
        options['title'] = {'text': escape(meeting_item.decision_item.name)}
        options['subtitle'] = {'text': subtitle}
        return options

    def factors_groups_scenario(self, meeting, scenario, stakeholder_ids):
        evaluations = Evaluation.get_evaluations_by_meeting(meeting) \
            .filter(meeting_item__in=scenario.meeting_items.all(), user_id__in=stakeholder_ids)
        aggregated_max_votes = scenario.meeting_items.count()
        options = self._factors_groups(evaluations, stakeholder_ids, aggregated_max_votes)
        items_names = scenario.meeting_items.values_list('decision_item__name', flat=True)
        items_text = u', '.join(items_names)
        stakeholders_text = get_stakeholders_group_names(stakeholder_ids)
        subtitle = u'<strong>{0}:</strong> {1}<br><strong>{2}:</strong> {3}'.format(
            _('Decision Items'),
            escape(items_text),
            _('Stakeholders Roles'),
            stakeholders_text
        )
        options['title'] = {'text': escape(scenario.name)}
        options['subtitle'] = {'text': subtitle}
        return options


    def get_decision_analysis_factor_ranking(self, meeting, factor, measure_values,
                                             measure_values_count, grouped_measure_values):
        value_rankings = dict()
        for meeting_item in meeting.meetingitem_set.order_by('decision_item__name'):
            item_evaluations = Evaluation.get_evaluations_by_meeting(meeting) \
                .filter(meeting_item=meeting_item, factor=factor) \
                .exclude(measure_value=None)

            max_evaluations = item_evaluations.count()

            rankings = list()
            for measure_value in measure_values:
                rankings.append({
                    'measure_value__id': measure_value.pk,
                    'measure_value__order': measure_value.order,
                    'votes': 0
                })

            votes_by_measure_value = item_evaluations \
                .values('measure_value__id', 'measure_value__order') \
                .annotate(votes=Count('measure_value')) \
                .order_by('measure_value__order')

            for measure_value_votes in votes_by_measure_value:
                for index, ranking in enumerate(rankings):
                    if ranking['measure_value__id'] == measure_value_votes['measure_value__id']:
                        rankings[index]['votes'] = measure_value_votes['votes']
                        break

            for index, ranking in enumerate(rankings):
                votes = int(ranking['votes'])
                percentage = get_votes_percentage(max_evaluations, votes, round_value=False)
                rankings[index]['percentage'] = round(percentage, 2)

            if measure_values_count <= 3:
                highest = rankings[0]
                lowest = rankings[-1]
                value_ranking = highest['percentage'] - lowest['percentage']
            else:
                highest_group = grouped_measure_values[0]
                highest_ids = map(lambda measure_value: measure_value.pk, highest_group)
                highest_sum = sum([r['percentage'] for r in rankings if r['measure_value__id'] in highest_ids])

                lowest_group = grouped_measure_values[-1]
                lowest_ids = map(lambda measure_value: measure_value.pk, lowest_group)
                lowest_sum = sum([r['percentage'] for r in rankings if r['measure_value__id'] in lowest_ids])

                value_ranking = highest_sum - lowest_sum

            value_rankings[meeting_item.pk] = round(value_ranking, 2)

        return value_rankings

    def decision_analysis(self, meeting, value_factor_x, value_factor_y):
        measure_values = meeting.measure.measurevalue_set.order_by('order')
        measure_values_count = measure_values.count()
        grouped_measure_values = None
        if measure_values_count > 3:
            grouped_measure_values = meeting.measure.get_grouped_measure_values()

        factor_x_ranking = self.get_decision_analysis_factor_ranking(meeting, value_factor_x, measure_values,
                                                                     measure_values_count, grouped_measure_values)

        factor_y_ranking = self.get_decision_analysis_factor_ranking(meeting, value_factor_y, measure_values,
                                                                     measure_values_count, grouped_measure_values)

        data = list()

        for mi in meeting.meetingitem_set.order_by('decision_item__name'):
            try:
                entry = {
                    'x': factor_x_ranking[mi.pk],
                    'y': factor_y_ranking[mi.pk],
                    'z': int(mi.decision_item.column_1),
                    'name': mi.decision_item.pk,
                    'description': mi.decision_item.name
                }
                data.append(entry)
            except (ValueError, TypeError):
                pass

        options = {
            'chart': {
                'type': 'bubble',
                'plotBorderWidth': 1,
                'zoomType': 'xy'
            },
            'legend': {
                'enabled': False
            },
            'title': {
                'text': 'Decision items analysis'
            },
            'xAxis': {
                'gridLineWidth': 1,
                'title': {
                    'text': value_factor_x.name
                }
            },
            'yAxis': {
                'startOnTick': False,
                'endOnTick': False,
                'title': {
                    'text': value_factor_y.name
                },
                'maxPadding': 0.2
            },
            'tooltip': {
                'useHTML': True,
                'headerFormat': '<table>',
                'pointFormat': '<tr><th colspan="2"><h3>{point.description}</h3></th></tr>' +
                    ('<tr><th>%s</th> <td>{point.x}</td></tr>' % value_factor_x.name) +
                    ('<tr><th>%s:</th> <td>{point.y}</td></tr>' % value_factor_y.name) +
                    '<tr><th>Size: </th> <td>{point.z} htp</td></tr>',
                'footerFormat': '</table>',
                'followPointer': True
            },
            'plotOptions': {
                'series': {
                    'dataLabels': {
                        'enabled': True,
                        'format': '{point.name}'
                    }
                }
            },
            'series': [{
                'data': data
            }]
        }
        return options
