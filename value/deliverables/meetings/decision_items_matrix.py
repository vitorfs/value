from colour import Color
from django.db.models import Count
from django.utils.safestring import mark_safe

from value.deliverables.meetings.models import Evaluation
from value.deliverables.meetings.utils import get_votes_percentage


class DecisionItemsMatrix(object):
    def __init__(self, meeting):
        self.meeting = meeting
        self.meeting_items = meeting.meetingitem_set \
            .select_related('decision_item') \
            .order_by('decision_item__name')
        self.factors = meeting.factors.all()

        self.measure_values = meeting.measure.measurevalue_set.order_by('order')
        self.measure_values_count = self.measure_values.count()

        self.grouped_measure_values = None
        # if self.measure_values_count > 3:
        #     self.grouped_measure_values = meeting.measure.get_grouped_measure_values()

        self.measure_values_lookup = self._get_measure_values_lookup()

    def _get_measure_values_lookup(self):
        measure_values_lookup = dict()
        measure_values_lookup[0] = {
            'color': '#ccc',
            'description': 'N/A'
        }
        if self.grouped_measure_values is not None:
            for index, group in enumerate(self.grouped_measure_values):
                color_1 = Color(group[0].color)
                color_2 = Color(group[-1].color)
                resulting_color = list(color_1.range_to(color_2, 5))
                measure_values_lookup[index + 1] = {
                    'color': resulting_color[2].get_hex(),
                    'description': ' / '.join(map(lambda x: x.description, group))
                }
        else:
            for measure_value in self.meeting.measure.measurevalue_set.values('id', 'description', 'color'):
                measure_values_lookup[measure_value['id']] = measure_value
        return measure_values_lookup

    def get_votes(self, meeting_item, factor):
        item_evaluations = Evaluation.get_evaluations_by_meeting(self.meeting) \
            .filter(meeting_item=meeting_item, factor=factor) \
            .exclude(measure_value=None)

        max_evaluations = item_evaluations.count()

        rankings = list()
        for measure_value in self.measure_values:
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

        return rankings

    def get_most_votes(self, meeting_item, factor):
        votes = self.get_votes(meeting_item, factor)
        highest = votes[0]
        multiple_highest = list()
        for vote in votes:
            if vote['votes'] == highest['votes']:
                multiple_highest.append(vote)
            elif vote['votes'] > highest['votes']:
                highest = vote
                multiple_highest = [highest,]  # erase old highest list and start over
        return multiple_highest

    def get_header(self):
        header = ['']
        header.append({
            'style': 'font-weight:bold;',
            'value': 'Value Ranking'
        })
        for factor in self.factors:
            group = u'[%s] ' % factor.group.name if factor.group is not None else ''
            name = u'%s%s' % (group, factor.name)
            entry = {
                'style': 'font-weight:bold;',
                'value': name
            }
            header.append(entry)
        return header

    def get_matrix(self):
        matrix = list()
        for mi in self.meeting_items.order_by('-value_ranking'):
            row = list()
            row.append({
                'style': 'font-weight:bold;',
                'value': mi.decision_item.name
            })
            row.append({
                'style': 'font-weight:bold;',
                'value': mark_safe(mi.value_ranking_as_html())
            })
            for factor in self.factors:
                votes = self.get_most_votes(mi, factor)

                if len(votes) > 1:
                    colors = list()
                    values = list()
                    for vote in votes:
                        measure_data = self.measure_values_lookup[vote['measure_value__id']]
                        colors.append(measure_data['color'])
                        values.append(measure_data['description'])
                    background = 'background-image: linear-gradient(%s)' % ','.join(colors)
                    names = u' / '.join(values)
                    value = u'{} ({}%)'.format(names, votes[0]['percentage'])
                else:
                    measure_data = self.measure_values_lookup[votes[0]['measure_value__id']]
                    background = 'background-color: %s' % measure_data['color']
                    value = u'{} ({}%)'.format(measure_data['description'], votes[0]['percentage'])
                entry = {
                    'style': ';'.join([background, 'text-align:center', 'font-weight:bold']),
                    'value': value,
                    'raw': votes[0]['percentage']
                }
                row.append(entry)
            matrix.append(row)

        return matrix
