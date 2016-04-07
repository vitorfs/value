# coding: utf-8

import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms.models import modelformset_factory

from value.deliverables.meetings.models import Meeting, MeetingItem, Rationale
from value.deliverables.meetings.forms import MeetingItemFinalDecisionForm
from value.deliverables.decorators import user_is_manager
from value.deliverables.meetings.decorators import user_is_meeting_stakeholder
from value.deliverables.meetings.utils import get_meeting_progress
from value.deliverables.meetings.forms import RationaleForm


@login_required
@user_is_meeting_stakeholder
def final_decision(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    MeetingItemFormset = modelformset_factory(MeetingItem, form=MeetingItemFinalDecisionForm, extra=0)
    meeting_items = meeting.meetingitem_set.select_related('decision_item').all().order_by('-meeting_decision')
    formset = MeetingItemFormset(queryset=meeting_items)
    return render(request, 'meetings/final_decision.html', {
        'meeting': meeting,
        'formset': formset})


@login_required
@user_is_manager
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


@login_required
@user_is_manager
@require_POST
@transaction.atomic
def save_final_decision_rationale(request, deliverable_id, meeting_id):
    pass


@login_required
@user_is_manager
@require_POST
@transaction.atomic
def save_final_decision_item_rationale(request, deliverable_id, meeting_id, meeting_item_id):
    try:
        mi = MeetingItem.objects.get(
            pk=meeting_item_id,
            meeting__id=meeting_id,
            meeting__deliverable__id=deliverable_id
        )

        text = request.POST.get('text', '').strip()

        if len(text):
            if not mi.meeting_decision_rationale:
                mi.meeting_decision_rationale = Rationale.objects.create(created_by=request.user)
                mi.save()

            form = RationaleForm(request.POST, instance=mi.meeting_decision_rationale)

            if form.is_valid():
                mi.meeting_decision_rationale = form.save(commit=False)
                mi.meeting_decision_rationale.updated_by = request.user
                mi.meeting_decision_rationale.save()
                mi.save()

                mi.meeting.deliverable.save()
                mi.meeting.calculate_meeting_related_rationales_count()
                context = get_meeting_progress(mi.meeting)
                return HttpResponse(json.dumps(context), content_type='application/json')
            else:
                return HttpResponseBadRequest(form['text'].errors.as_text())
        elif mi.meeting_decision_rationale:
            rationale = mi.meeting_decision_rationale
            mi.meeting_decision_rationale = None
            mi.save()

            rationale.delete()
            mi.meeting.deliverable.save()
            mi.meeting.calculate_meeting_related_rationales_count()
            context = get_meeting_progress(mi.meeting)
            return HttpResponse(json.dumps(context), content_type='application/json')

    except MeetingItem.DoesNotExist:
        return HttpResponseBadRequest(_('An error ocurred while trying to save your data.'))