from django.db.models import Count

from value.deliverables.meetings.models import Evaluation
from value.deliverables.meetings.utils import get_votes_percentage


def calc_value_ranking(meeting, stakeholders_ids=None):
    if stakeholders_ids is None:
        stakeholders_ids = meeting.meetingstakeholder_set.values_list('stakeholder_id', flat=True)

    measure = meeting.measure
    stakeholders_count = len(stakeholders_ids)
    factors_count = meeting.factors.count()
    max_evaluations = stakeholders_count * factors_count

    value_rankings = list()

    for meeting_item in meeting.meetingitem_set.all():
        item_evaluations = Evaluation.get_evaluations_by_meeting(meeting) \
            .filter(meeting_item=meeting_item, user__in=stakeholders_ids)

        rankings = item_evaluations \
            .values('measure_value__id', 'measure_value__order') \
            .annotate(votes=Count('measure_value')) \
            .order_by('measure_value__order')

        rankings = list(rankings)

        for index, ranking in enumerate(rankings):
            votes = int(ranking['votes'])
            percentage = get_votes_percentage(max_evaluations, votes, round_value=False)
            rankings[index]['percentage'] = round(percentage, 2)

        if measure.measurevalue_set.count() <= 3:
            highest = rankings[0]
            lowest = rankings[-1]
            value_ranking = highest['percentage'] - lowest['percentage']
        else:
            grouped_measure_values = measure.get_grouped_measure_values()
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
    return value_rankings


def calc_value_ranking_per_stakeholder_group(meeting):
    value_rankings_groups = list()
    groups = meeting.get_stakeholder_groups()
    for group, stakeholders in groups.items():
        stakeholders_ids = [stakeholder.id for stakeholder in stakeholders]
        value_rankings = calc_value_ranking(meeting, stakeholders_ids)
        value_rankings_groups.append({
            'group': group,
            'value_rankings': value_rankings
        })
    return value_rankings_groups


def calc_value_ranking_per_stakeholder(meeting):
    value_rankings_groups = list()
    meeting_stakeholders = meeting.meetingstakeholder_set.select_related('stakeholder__profile').all()
    for meeting_stakeholder in meeting_stakeholders:
        stakeholders_ids = [meeting_stakeholder.stakeholder.pk,]
        value_rankings = calc_value_ranking(meeting, stakeholders_ids)
        value_rankings_groups.append({
            'group': meeting_stakeholder.stakeholder.profile.get_display_name(),
            'value_rankings': value_rankings
        })
    return value_rankings_groups
