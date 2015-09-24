# coding: utf-8

from django import template
from django.utils.html import escape

from value.deliverables.meetings.models import MeetingItem

register = template.Library()


@register.filter('meeting_item')
def meeting_item(meeting_item_id):
    try:
        item = MeetingItem.objects.get(pk=meeting_item_id)
        return item
    except MeetingItem.DoesNotExist:
        return None

@register.simple_tag
def display_ranking(ranking_set):
    ranking_set = ranking_set.select_related('measure_value')
    html = u'<div class="progress" style="margin-bottom: 0">'
    for ranking in ranking_set:
        progress_bar = u'''<div class="progress-bar" style="width: {0}%; background-color: {1};">
      <span class="measure-percent" data-measure-id="{2}">{3}</span>%
    </div>'''.format(ranking.percentage_votes, 
                     ranking.measure_value.color, 
                     ranking.measure_value.pk, 
                     ranking.get_percentage_votes_display())
        html += progress_bar
    html += u'</div>'
    return html