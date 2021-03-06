# coding: utf-8

import json

from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms.models import modelformset_factory
from django.utils.translation import ugettext as _

from value.deliverables.meetings.models import Meeting, MeetingItem, Rationale
from value.deliverables.meetings.forms import MeetingItemFinalDecisionForm, ScenarioFinalDecision
from value.deliverables.decorators import user_is_manager
from value.deliverables.meetings.decorators import user_is_meeting_stakeholder
from value.deliverables.meetings.utils import get_meeting_progress
from value.deliverables.meetings.forms import RationaleForm


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
def set_scenario_final_decision(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    form = ScenarioFinalDecision(meeting=meeting, data=request.POST)
    if form.is_valid():
        form.set_final_decision()
        messages.success(request, _('The scenario "%s" was saved as the final decision.') % form.cleaned_data.get('scenario').name)
    else:
        messages.error(request, _('An error occurred. Please try again later.'))
    return redirect('deliverables:meetings:final_decision', deliverable_id=deliverable_id, meeting_id=meeting_id)


@login_required
@user_is_manager
@require_POST
@transaction.atomic
def save_final_decision_rationale(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    if meeting.meeting_decision_rationale:
        rationale = meeting.meeting_decision_rationale
    else:
        rationale = Rationale.objects.create(created_by=request.user)
        meeting.meeting_decision_rationale = rationale
        meeting.save()

    form = RationaleForm(request.POST, instance=rationale)
    if form.is_valid():
        rationale = form.save()
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


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
        else:
            context = get_meeting_progress(mi.meeting)
            return HttpResponse(json.dumps(context), content_type='application/json')

    except MeetingItem.DoesNotExist:
        return HttpResponseBadRequest(_('An error ocurred while trying to save your data.'))
