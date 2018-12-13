# coding: utf-8

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from value.deliverables.meetings.models import Meeting, MeetingItem, Scenario


def rationales(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    return render(request, 'meetings/rationales/meeting.html', {'meeting': meeting})


@login_required
def meeting_item_rationale(request, deliverable_id, meeting_id, meeting_item_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    meeting_item = get_object_or_404(MeetingItem, pk=meeting_item_id)
    return render(request, 'meetings/rationales/meeting_item.html', {
        'meeting': meeting,
        'meeting_item': meeting_item
    })


@login_required
def scenario_rationale(request, deliverable_id, meeting_id, scenario_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    rationales = list()
    return render(request, 'meetings/rationales/meeting_item.html', {
        'meeting': meeting,
        'scenario': scenario,
        'rationales': rationales
    })
