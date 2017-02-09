import itertools
import operator

from colour import Color

from value.deliverables.meetings.utils import get_votes_percentage


class StakeholdersAgreement(object):

    def __init__(self, meeting, group_measures=False):
        self.group_measures = group_measures
        self.meeting = meeting
        self.meeting_stakeholders = meeting.meetingstakeholder_set \
            .select_related('stakeholder', 'stakeholder__profile') \
            .order_by('stakeholder__first_name', 'stakeholder__last_name', 'stakeholder__username')
        self.meeting_items = meeting.meetingitem_set \
            .select_related('decision_item') \
            .order_by('decision_item__name')
        self.dataset = self._generate_evaluaton_dataset(group_measures)

    def _generate_evaluaton_dataset(self, group_measures):
        '''
        Following a sample of the output of the dataset, considering:

        * 2 stakeholders
        * 6 decision items
        * 9 value factors
        * 3 measure values

        {
          1:
          {
            324: (2, [(3, 2), (2, 1), (2, 1), (2, 1), (3, 2), (3, 2), (1, 0), (2, 1), (1, 0)]),
            325: (1, [(1, 0), (1, 0), (2, 1), (1, 0), (3, 2), (3, 2), (3, 2), (2, 1), (2, 1)]),
            326: (2, [(3, 2), (2, 1), (1, 0), (2, 1), (2, 1), (2, 1), (1, 0), (2, 1), (1, 0)]),
            327: (3, [(1, 0), (3, 2), (3, 2), (2, 1), (2, 1), (3, 2), (3, 2), (3, 2), (3, 2)]),
            328: (3, [(3, 2), (3, 2), (3, 2), (2, 1), (2, 1), (3, 2), (3, 2), (3, 2), (2, 1)]),
            329: (2, [(3, 2), (3, 2), (1, 0), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (1, 0)])
          },
         2:
          {
            324: (1, [(1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (0, 99)]),
            325: (2, [(1, 0), (1, 0), (2, 1), (2, 1), (2, 1), (3, 2), (3, 2), (3, 2), (2, 1)]),
            326: (1, [(1, 0), (1, 0), (1, 0), (3, 2), (1, 0), (2, 1), (3, 2), (1, 0), (2, 1)]),
            327: (3, [(2, 1), (3, 2), (1, 0), (2, 1), (3, 2), (2, 1), (1, 0), (3, 2), (3, 2)]),
            328: (2, [(3, 2), (2, 1), (1, 0), (2, 1), (2, 1), (1, 0), (1, 0), (2, 1), (3, 2)]),
            329: (1, [(1, 0), (2, 1), (1, 0), (1, 0), (3, 2), (3, 2), (3, 2), (1, 0), (2, 1)])
          }
        }

        The outmost items in the dataset (1 and 2) are keys represented by the ID of the stakeholder
        Accessing the dict using the ID of a stakeholder (dataset[1]) returns a new dict, this time identified by
        the IDs of the decision items (324, 325, 326, 327, 328, 329 are all IDs).
        Acessing one decision item (dataset[1][324]) returns a tuple, where the first item is the overall evaluation of
        this stakeholder.
        In the first row, dataset[1][324] = (2, [(3, 2), (2, 1), (2, 1), (2, 1), (3, 2), (3, 2), (1, 0), (2, 1), (1, 0)])
        means `2` was the most common measure value (Neutral votes). The second item in the tuple is a list, composed by
        tuples that represent: measure_value_id, measure_value_order.
        The measure_value_id is used to compare, and the order is used to set the priority of the most important measure
        value.
        When the measure_value_order is set to `99`, means this is related to empty (N/A) measure value, where the
        stakeholder didn't give any assessment.
        '''

        meeting_factors = self.meeting.factors.values('id', 'name').order_by('group', 'name')

        ''' Initialize the dataset, adding a default of 0 to all evaluations '''
        dataset = dict()
        for ms in self.meeting_stakeholders:
            dataset[ms.stakeholder.pk] = dict()
            for mi in self.meeting_items:
                dataset[ms.stakeholder.pk][mi.pk] = list()
                for mf in meeting_factors:
                    # set 0 as a invalid id for measure value, and 99 as a very high order, so to have least priority
                    dataset[ms.stakeholder.pk][mi.pk].append((0, 99))

        ''' Create a lookup for the value factors, for fast access '''
        factors_lookup = dict()
        for index, factor in enumerate(meeting_factors):
            factors_lookup[factor['id']] = index

        ''' Create a lookup for measure values, for fast access '''
        measure_values_lookup = None
        if group_measures:
            measure_values_lookup = self.get_measure_values_lookup()

        ''' Generate the evaluation matrix, filling the dataset with all the existing evaluations '''
        evaluations = self.meeting.get_evaluations() \
            .select_related('measure_value') \
            .values_list('user', 'meeting_item', 'factor', 'measure_value', 'measure_value__order')
        for e in evaluations:
            user_index = e[0]
            item_index = e[1]
            factor_index = factors_lookup[e[2]]

            if group_measures:
                grouped_measure_value = measure_values_lookup[e[3]]
                measure_value = (grouped_measure_value, e[4], )
            else:
                measure_value = (e[3], e[4],)

            dataset[user_index][item_index][factor_index] = measure_value

        ''' Append to the dataset the overall evaluation of each item '''
        for msk in dataset.keys():  # meeting stakeholder key
            for mik in dataset[msk].keys():  # meeting item key
                top_vote = self._get_most_common_item_ordered(dataset[msk][mik])
                dataset[msk][mik] = (top_vote, dataset[msk][mik], )

        return dataset

    def _get_most_common_item_ordered(self, votes_list):
        smie = sorted(votes_list, key=lambda m: m[1])  # sorted meeting item evaluations
        groups = itertools.groupby(smie, key=lambda m: (m[0], m[1],))
        groups_count = map(lambda x: x[0] + (len(list(x[1])),), groups)
        groups_count.sort(key=lambda x: (-x[2], x[1]))
        return groups_count[0][0]

    def get_measure_values_lookup(self):
        '''
        Generate index for grouping measure values
        In the grouping the following values means:
        Odd number of values: 1 = positive, 2 = neutral, 3 = negative
        Even number of values: 1 = positive, 2 = negative
        '''
        measure_values_lookup = dict()
        grouped_measure_value = self.meeting.measure.get_grouped_measure_values()
        for index, group in enumerate(grouped_measure_value):
            for measure_value in group:
                measure_values_lookup[measure_value.pk] = (index + 1)
        return measure_values_lookup

    def get_stakeholders_opinion(self):
        measure_values_lookup = dict()
        measure_values_lookup[0] = {
            'color': '#ccc',
            'description': 'N/A'
        }
        if self.group_measures:
            grouped_measure_value = self.meeting.measure.get_grouped_measure_values()
            for index, group in enumerate(grouped_measure_value):
                color_1 = Color(group[0].color)
                color_2 = Color(group[-1].color)
                resulting_color = list(color_1.range_to(color_2, 5))
                measure_values_lookup[index + 1] = {
                    'color': resulting_color[2].get_hex(),
                    'description': '/'.join(map(lambda x: x.description, group))
                }
        else:
            for measure_value in self.meeting.measure.measurevalue_set.values('id', 'description', 'color'):
                measure_values_lookup[measure_value['id']] = measure_value

        stakeholders_opinion = list()
        for mi in self.meeting_items:
            meeting_item_row = (mi, list())
            for ms in self.meeting_stakeholders:
                winner = self.dataset[ms.stakeholder.pk][mi.pk][0]
                votes = self.dataset[ms.stakeholder.pk][mi.pk][1]
                winner_count = len(filter(lambda x: x[0] == winner, votes))
                winner_percentage = get_votes_percentage(len(votes), winner_count)
                meeting_item_row[1].append({
                    'color': measure_values_lookup[winner]['color'],
                    'description': measure_values_lookup[winner]['description'],
                    'percentage': winner_percentage
                })

            mi_dataset = list()
            for stakeholder_id, stakeholder_meeting_items in self.dataset.iteritems():
                mi_dataset += stakeholder_meeting_items[mi.pk][1]

            overall_winner = self._get_most_common_item_ordered(mi_dataset)
            overall_winner_count = len(filter(lambda x: x[0] == overall_winner, mi_dataset))
            overall_winner_percentage = get_votes_percentage(len(mi_dataset), overall_winner_count)

            meeting_item_row[1].append({
                'color': measure_values_lookup[overall_winner]['color'],
                'description': measure_values_lookup[overall_winner]['description'],
                'percentage': overall_winner_percentage
            })
            stakeholders_opinion.append(meeting_item_row)
        return stakeholders_opinion

    def matrix_by_factors(self):
        meeting_factors_count = self.meeting.factors.count()

        ''' Calculate the level of agreement between the stakeholders '''
        factors_indexes = range(0, meeting_factors_count)
        max_agreement = self.meeting_items.count() * meeting_factors_count
        factors_agreement = list()

        for ms_1 in self.meeting_stakeholders:
            factors_agreement_row = (ms_1, list())
            for ms_2 in self.meeting_stakeholders:
                agreement_sum = 0
                for mi in self.meeting_items:
                    for i in factors_indexes:
                        if self.dataset[ms_1.stakeholder.pk][mi.pk][1][i][0] == self.dataset[ms_2.stakeholder.pk][mi.pk][1][i][0]:
                            agreement_sum += 1
                # Translate the raw result into percentages
                percentage_agreement_sum = get_votes_percentage(max_agreement, agreement_sum)
                factors_agreement_row[1].append((ms_2, percentage_agreement_sum, ))
            factors_agreement.append(factors_agreement_row)

        return factors_agreement


    def matrix_by_items(self):
        ''' Calculate the level of agreement between the stakeholders based on the overall decision items value '''
        max_agreement = self.meeting_items.count()
        items_agreement = list()

        for ms_1 in self.meeting_stakeholders:
            items_agreement_row = (ms_1, list())
            for ms_2 in self.meeting_stakeholders:
                agreement_sum = 0
                for mi in self.meeting_items:
                    # The `self.dataset[ms_1.stakeholder.pk][mi.pk][0]` returns the most used measure value for a
                    # given item a given stakeholder evaluated
                    if self.dataset[ms_1.stakeholder.pk][mi.pk][0] == self.dataset[ms_2.stakeholder.pk][mi.pk][0]:
                        agreement_sum += 1
                # Translate the raw result into percentages
                percentage_agreement_sum = get_votes_percentage(max_agreement, agreement_sum)
                items_agreement_row[1].append((ms_2, percentage_agreement_sum, ))
            items_agreement.append(items_agreement_row)

        return items_agreement
