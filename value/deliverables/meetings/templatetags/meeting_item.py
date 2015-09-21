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
