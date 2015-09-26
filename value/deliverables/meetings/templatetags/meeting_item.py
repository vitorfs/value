# coding: utf-8

from django import template
from django.utils.html import escape
from django.core.urlresolvers import reverse

from value.deliverables.meetings.models import MeetingItem, Scenario
from value.deliverables.meetings.utils import format_percentage

register = template.Library()


@register.filter('meeting_item')
def meeting_item(meeting_item_id):
    try:
        item = MeetingItem.objects.get(pk=meeting_item_id)
        return item
    except MeetingItem.DoesNotExist:
        return None

@register.simple_tag
def display_evaluation_summary(instance):
    html = u'<div class="progress" style="margin-bottom: 0">'
    if isinstance(instance, MeetingItem):
        ranking_set = instance.ranking_set.all().select_related('measure_value')
        for ranking in ranking_set:
            progress_bar = u'''<div class="progress-bar" style="width: {0}%; background-color: {1};">
              <span class="measure-percent" data-measure-id="{2}" data-percentage="{0}">{3}</span>%
            </div>'''.format(ranking.percentage_votes, 
                             ranking.measure_value.color, 
                             ranking.measure_value.pk, 
                             ranking.get_percentage_votes_display())
            html += progress_bar
    html += u'</div>'
    return html

@register.simple_tag
def display_ranking_label(ranking):
    label = 'label-success'
    if ranking < 0:
        label = 'label-danger'
    elif ranking == 0:
        label = 'label-warning'        
    html = u'<span class="label {0} pull-right" style="margin-right: 10px; margin-top: 2px;">{1}</span>'.format(label, format_percentage(ranking))
    return html

@register.simple_tag
def display_info_button(meeting_item):
    remote = reverse('deliverables:details_decision_item', args=(meeting_item.meeting.deliverable.pk, meeting_item.decision_item.pk))
    html = u'''<span data-toggle="tooltip" title="Click to view details" data-container="body" style="margin-left: 5px;">
            <a href="javascript:void(0);" class="btn-details js-decision-item-details" data-toggle="modal" data-target="#modal-decision-item-details" data-remote-url="{0}">
              <span class="glyphicon glyphicon-info-sign"></span>
            </a>
          </span>'''.format(remote)
    return html
