import operator
import pprint

from django.contrib.auth.models import User
from django.db.models import Count
from django.utils.html import escape

from value.factors.models import Factor
from value.deliverables.meetings.models import Meeting, MeetingItem, Evaluation


pp = pprint.PrettyPrinter(indent=4, depth=6)

def get_stakeholders_group_names(stakeholder_ids):
    stakeholders = User.objects.filter(id__in=stakeholder_ids)
    groups = set()
    for stakeholder in stakeholders:
        for group in stakeholder.groups.all():
            groups.add(group.name)
    groups_text = u', '.join(groups)
    return escape(groups_text)

class Highcharts(object):

    label_style = { 'fontSize': '13px', 'fontFamily': '"Helvetica Neue", Helvetica, Arial, sans-serif' }

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
            votes = result['count']
            if max_votes != 0:
                percentage = round((votes / float(max_votes)) * 100.0, 2)
            else:
                percentage = 0.0
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
            if max_input != 0:
                percentage = round((votes / float(max_input)) * 100.0, 2)
            else:
                percentage = 0.0
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
            if max_votes != 0:
                percentage = round((votes / float(max_votes)) * 100.0, 2)
            else:
                percentage = 0.0
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
            'yAxis': { 'min': 0, 'title': { 'text': 'Number of votes' } },
            'legend': { 'reversed': True },
            'plotOptions': { 'series': { 'stacking': stacking }},
            'exporting': { 'enabled': False },
            'series': series
        }

        return options


    def decision_items_overview(self, meeting, chart, stakeholder_ids):
        stakeholder_ids = list(set(stakeholder_ids))
        evaluations = Evaluation.get_evaluations_by_meeting(meeting).filter(user_id__in=stakeholder_ids)
        measure = evaluations[0].measure
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
                percentage = 0.0
                if max_votes != 0:
                    percentage = round((votes / float(max_votes)) * 100.0, 2)
                serie_data.append(percentage)
            series.append({ 'name': measure_value.description, 'data': serie_data, 'color': measure_value.color })

        options = self._base_stacked_chart(categories, series, chart)
        groups_text = get_stakeholders_group_names(stakeholder_ids)
        options['title'] = { 'text': u'Decision Items Overview' }
        options['subtitle'] = { 'text': u'{0} opinion'.format(groups_text) }
        return options


    def features_selection_stacked_chart(self, meeting_id, meeting_item_id, chart, stakeholder_ids):
        
        meeting = Meeting.objects.get(pk=meeting_id)
        meeting_item = MeetingItem.objects.get(pk=meeting_item_id)
        evaluations = Evaluation.get_evaluations_by_meeting(meeting).filter(meeting_item=meeting_item, user_id__in=stakeholder_ids)

        if evaluations:

            data = {}

            for evaluation in evaluations:
                if evaluation.factor.group:
                    label = u'<strong style="text-decoration: underline;">{0}:</strong> {1}'.format(evaluation.factor.group.name, evaluation.factor.name)
                else:
                    label = evaluation.factor.name
                data[label] = {}
                for value in evaluation.factor.measure.measurevalue_set.all():
                    data[label][value.description] = 0

            for evaluation in evaluations:
                if evaluation.factor.group:
                    label = u'<strong style="text-decoration: underline;">{0}:</strong> {1}'.format(evaluation.factor.group.name, evaluation.factor.name)
                else:
                    label = evaluation.factor.name
                data[label][evaluation.measure_value.description] = data[label][evaluation.measure_value.description] + 1

            sorted_data = sorted(data.items(), key=operator.itemgetter(0))

            categories = []
            for factor in sorted_data:
                categories.append(factor[0])

            measure = evaluations[0].measure

            series = []
            for value in measure.measurevalue_set.all():
                serie_data = []
                for factor in sorted_data:
                    serie_data.append(factor[1][value.description])
                series.append({ 'name': value.description, 'data': serie_data, 'color': value.color })

            options = self._base_stacked_chart(categories, series, chart)
            groups_text = get_stakeholders_group_names(stakeholder_ids)
            options['title'] = { 'text': u'{0} Value Factors Comparison'.format(meeting_item.decision_item.name) }
            options['subtitle'] = { 'text': u'{0} opinion'.format(groups_text) }
            return options

        return {}

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

    def features_acceptance_simple_treemap(self, instance_id, item_id, stakeholder_ids):
        instance = Meeting.objects.get(pk=instance_id)
        item = MeetingItem.objects.get(pk=item_id)
        evaluations = Evaluation.get_evaluations_by_meeting(instance).filter(meeting_item=item, user_id__in=stakeholder_ids)

        vqs = evaluations.values('measure_value__description', 'measure_value__color').annotate(value=Count('measure_value__description')).order_by()
        data = [kv for kv in vqs]
        for d in data:
            d['name'] = d.pop('measure_value__description')
            d['color'] = d.pop('measure_value__color')

        options = self._base_treemap(data)
        options['title'] = { 'text': u'{0} Acceptance'.format(item.decision_item.name) }
        groups_text = get_stakeholders_group_names(stakeholder_ids)
        options['subtitle'] = { 'text': u'{0} opinion'.format(groups_text) }

        return options

    def features_acceptance_detailed_treemap(self, instance_id, item_id, stakeholder_ids):
        instance = Meeting.objects.get(pk=instance_id)
        item = MeetingItem.objects.get(pk=item_id)
        evaluations = Evaluation.get_evaluations_by_meeting(instance).filter(meeting_item=item, user_id__in=stakeholder_ids)

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

        options = self._base_treemap(data)
        options['title'] = { 'text': u'{0} Acceptance'.format(item.decision_item.name) }
        groups_text = get_stakeholders_group_names(stakeholder_ids)
        options['subtitle'] = { 'text': u'{0} opinion'.format(groups_text) }
        
        return options

    def features_acceptance_pie_chart_drilldown(self, instance_id, item_id, stakeholder_ids):
        instance = Meeting.objects.get(pk=instance_id)
        item = MeetingItem.objects.get(pk=item_id)
        evaluations = Evaluation.get_evaluations_by_meeting(instance).filter(meeting_item=item, user_id__in=stakeholder_ids)

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

        groups_text = get_stakeholders_group_names(stakeholder_ids)
        options = {
                'chart': { 'type': 'pie' },
                'title': { 'text': u'{0} Acceptance'.format(escape(item.decision_item.name)) },
                'subtitle': { 'text': u'{0} opinion. Click the slices to view value factors.'.format(groups_text) },
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
                    'series': drilldownSeries
                }
            }
        return options

    def features_acceptance_bubbles(self, meeting_id, meeting_item_id, stakeholder_ids):
        options = {
            'chart': { 'type': 'bubble', 'zoomType': 'xy' },
            'title': { 'text': '' },
            'exporting': { 'enabled': False },
            'series': [{
                'name': 'Test',
                'data': [[97, 36, 79], [94, 74, 60], [68, 76, 58], [64, 87, 56], [68, 27, 73], [74, 99, 42], [7, 93, 87], [51, 69, 40], [38, 23, 33], [57, 86, 31]]
            }, {
                'data': [[25, 10, 87], [2, 75, 59], [11, 54, 8], [86, 55, 93], [5, 3, 58], [90, 63, 44], [91, 33, 17], [97, 3, 56], [15, 67, 48], [54, 25, 81]]
            }, {
                'data': [[47, 47, 21], [20, 12, 4], [6, 76, 91], [38, 30, 60], [57, 98, 64], [61, 17, 80], [83, 60, 13], [67, 78, 75], [64, 12, 10], [30, 77, 82]]
            }]
        }

        return options

    def factors_groups(self, meeting_item, stakeholder_ids):
        evaluations = Evaluation.get_evaluations_by_meeting(meeting_item.meeting) \
                .filter(meeting_item=meeting_item, user_id__in=stakeholder_ids)

        categories = evaluations.values_list('factor__group__name', flat=True).distinct().order_by('factor__group__name')

        measure = meeting_item.meeting.deliverable.measure
        series = []
        for measure_value in measure.measurevalue_set.all():
            serie = { 
                    'name': measure_value.description, 
                    'color': measure_value.color, 
                    'pointPlacement': 'on', 
                    'data': [] 
                }
            for category in categories:
                count = evaluations.filter(factor__group__name=category, measure_value=measure_value).count()
                serie['data'].append(count)
            series.append(serie)

        categories = [category if category else 'No group' for category in categories]

        options = {
            'chart': { 'polar': True, 'type': 'line' },
            'title': { 'text': escape(meeting_item.decision_item.name) },
            'xAxis': {
                'categories': list(categories),
                'tickmarkPlacement': 'on',
                'lineWidth': 0
            },
            'yAxis': {
                'gridLineInterpolation': 'polygon',
                'min': 0
            },
            'tooltip': {
                'shared': True,
                'pointFormat': '<span style="color:{series.color}">{series.name}: <b>{point.y} votes</b><br/>'
            },
            'exporting': { 'enabled': False },
            'series': series
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
