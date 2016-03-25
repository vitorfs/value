# coding: utf-8

import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms.models import modelformset_factory

from value.deliverables.meetings.models import Meeting, MeetingItem
from value.deliverables.meetings.forms import MeetingItemFinalDecisionForm


@login_required
def final_decision(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    MeetingItemFormset = modelformset_factory(MeetingItem, form=MeetingItemFinalDecisionForm, extra=0)
    meeting_items = meeting.meetingitem_set.select_related('decision_item').all().order_by('-meeting_decision')
    formset = MeetingItemFormset(queryset=meeting_items)
    return render(request, 'meetings/final_decision.html', {
        'meeting': meeting,
        'formset': formset})


@login_required
@require_POST
@transaction.atomic
def save_final_decision(request, deliverable_id, meeting_id):
    MeetingItemFormset = modelformset_factory(MeetingItem, form=MeetingItemFinalDecisionForm, extra=0)
    formset = MeetingItemFormset(request.POST)
    errors = list()
    for form in formset:
        if form.is_valid():
            form.save()
        else:
            errors.append(form.instance.pk)
    if any(errors):
        dump = json.dumps(errors)
        return HttpResponseBadRequest(dump, content_type='application/json')
    return HttpResponse()
