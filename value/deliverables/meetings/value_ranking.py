from django.db.models import Count

from value.deliverables.meetings.models import Evaluation
from value.deliverables.meetings.utils import get_votes_percentage

from django.utils.translation import gettext as _


def vrank(total, *values):
    fib = list()
    a, b = 1, 1
    for i in range(total):
        a, b = b, a + b
        fib.append(a)
    fib.reverse()
    rsum = 0.0
    for value in values:
        index = value - 1
        rsum += fib[index]
    rsum = rsum / len(values)
    rank = rsum / fib[0]
    return rank


def _calc_value_ranking(meeting, meeting_items, measure_values_count, factors_count,
                        stakeholders_ids, measure_values, grouped_measure_values):
    stakeholders_count = len(stakeholders_ids)
    max_evaluations = stakeholders_count * factors_count

    value_rankings = list()

    for meeting_item in meeting_items:
        item_evaluations = Evaluation.get_evaluations_by_meeting(meeting) \
            .filter(meeting_item=meeting_item, user__in=stakeholders_ids)

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

        value_rankings.append({
            'meeting_item': meeting_item,
            'value_ranking': value_ranking
        })

    value_rankings = sorted(value_rankings, key=lambda v: v['value_ranking'], reverse=True)
    for index, entry in enumerate(value_rankings):
        value_rankings[index]['ranking'] = index + 1
    return value_rankings


def calc_value_ranking_all(meeting):
    meeting_items = meeting.meetingitem_set.all()
    factors_count = meeting.factors.count()
    measure_values = meeting.measure.measurevalue_set.order_by('order')
    measure_values_count = measure_values.count()

    grouped_measure_values = None
    if measure_values_count > 3:
        grouped_measure_values = meeting.measure.get_grouped_measure_values()

    stakeholders_ids = meeting.meetingstakeholder_set.values_list('stakeholder_id', flat=True)
    value_rankings = _calc_value_ranking(meeting, meeting_items, measure_values_count, factors_count,
                                         stakeholders_ids, measure_values, grouped_measure_values)
    return value_rankings


def calc_value_ranking_per_stakeholder_group(meeting):
    value_rankings_groups = list()
    meeting_items = meeting.meetingitem_set.all()
    factors_count = meeting.factors.count()
    measure_values = meeting.measure.measurevalue_set.order_by('order')
    measure_values_count = measure_values.count()

    grouped_measure_values = None
    if measure_values_count > 3:
        grouped_measure_values = meeting.measure.get_grouped_measure_values()

    groups = meeting.get_stakeholder_groups()

    for group, stakeholders in groups.items():
        stakeholders_ids = [stakeholder.id for stakeholder in stakeholders]
        value_rankings = _calc_value_ranking(meeting, meeting_items, measure_values_count, factors_count,
                                             stakeholders_ids, measure_values, grouped_measure_values)
        value_rankings_groups.append({
            'group': group,
            'value_rankings': value_rankings
        })

    aggregated_ranking = calculate_aggregated_ranking(value_rankings_groups)
    value_rankings_groups = set_balanced_value_ranking(aggregated_ranking, value_rankings_groups)

    for index, group in enumerate(value_rankings_groups):
        value_rankings_groups[index]['value_rankings'] = sorted(
            value_rankings_groups[index]['value_rankings'], key=lambda v: v['balanced_value_ranking'], reverse=True
        )

    return value_rankings_groups


def calc_value_ranking_per_stakeholder(meeting):
    value_rankings_groups = list()
    meeting_items = meeting.meetingitem_set.all()
    measure_values = meeting.measure.measurevalue_set.order_by('order')
    measure_values_count = measure_values.count()
    factors_count = meeting.factors.count()
    grouped_measure_values = None

    if measure_values_count > 3:
        grouped_measure_values = meeting.measure.get_grouped_measure_values()

    meeting_stakeholders = meeting.meetingstakeholder_set.select_related('stakeholder__profile').all()

    for meeting_stakeholder in meeting_stakeholders:
        stakeholders_ids = [meeting_stakeholder.stakeholder.pk,]
        value_rankings = _calc_value_ranking(meeting, meeting_items, measure_values_count, factors_count,
                                             stakeholders_ids, measure_values, grouped_measure_values)
        value_rankings_groups.append({
            'group': meeting_stakeholder.stakeholder.profile.get_display_name(),
            'value_rankings': value_rankings
        })

    aggregated_ranking = calculate_aggregated_ranking(value_rankings_groups)
    value_rankings_groups = set_balanced_value_ranking(aggregated_ranking, value_rankings_groups)

    for index, group in enumerate(value_rankings_groups):
        value_rankings_groups[index]['value_rankings'] = sorted(
            value_rankings_groups[index]['value_rankings'], key=lambda v: v['balanced_value_ranking'], reverse=True
        )

    return value_rankings_groups


def calculate_aggregated_ranking(value_rankings_groups):
    meeting_items = [entry['meeting_item'] for entry in value_rankings_groups[0]['value_rankings']]
    aggregated_ranking = {}
    for meeting_item in meeting_items:
        aggregated_ranking[meeting_item.pk] = {
            'meeting_item': meeting_item,
            'value_ranking': meeting_item.value_ranking,
            'values': []
        }

    for group in value_rankings_groups:
        for ranking in group['value_rankings']:
            meeting_item_id = ranking['meeting_item'].pk
            value = ranking['ranking']
            aggregated_ranking[meeting_item_id]['values'].append(value)

    total = len(meeting_items)
    for meeting_item_id, rankings_dict in aggregated_ranking.iteritems():
        values = rankings_dict['values']
        balanced_value_ranking = vrank(total, *values)
        aggregated_ranking[meeting_item_id]['balanced_value_ranking'] = balanced_value_ranking
        aggregated_ranking[meeting_item_id]['balanced_value_ranking_display'] = round(balanced_value_ranking * 100.0, 2)

    return aggregated_ranking


def set_balanced_value_ranking(aggregated_ranking, value_rankings_groups):
    for index, group in enumerate(value_rankings_groups):
        for child_index, ranking in enumerate(group['value_rankings']):
            meeting_item_id = ranking['meeting_item'].pk
            balanced_value_ranking = aggregated_ranking[meeting_item_id]['balanced_value_ranking']
            balanced_value_ranking_display = aggregated_ranking[meeting_item_id]['balanced_value_ranking_display']
            value_rankings_groups[index]['value_rankings'][child_index]['balanced_value_ranking'] = balanced_value_ranking
            value_rankings_groups[index]['value_rankings'][child_index]['balanced_value_ranking_display'] = balanced_value_ranking_display

    return value_rankings_groups
