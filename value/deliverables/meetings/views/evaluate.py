# coding: utf-8

import json

from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.utils.translation import ugettext as _

from value.factors.models import Factor
from value.measures.models import Measure, MeasureValue
from value.deliverables.meetings.forms import RationaleForm
from value.deliverables.meetings.models import Meeting, MeetingItem, MeetingStakeholder, Evaluation
from value.deliverables.meetings.utils import get_meeting_progress


@login_required
def evaluate(request, deliverable_id, meeting_id, template_name='meetings/evaluate.html'):
    try:
        meeting = Meeting.objects \
            .select_related('deliverable', 'measure') \
            .prefetch_related('factors__group', 'factors__measure') \
            .get(pk=meeting_id, deliverable__id=deliverable_id)
    except Meeting.DoesNotExist:
        raise Http404

    factors = meeting.factors.order_by('group__name', 'name')
    measure = meeting.measure
    measure_values = measure.measurevalue_set.all()

    count = measure_values.count()
    grid_space = 60.0
    if count > 5:
        grid_space = 75.0
    if count > 0:
        size = grid_space / count
        relative_col_size = '{0}%'.format(size)
    else:
        relative_col_size = 'auto'

    evaluations = Evaluation.get_user_evaluations_by_meeting(user=request.user, meeting=meeting) \
        .select_related(
            'meeting',
            'meeting_item',
            'user',
            'factor',
            'factor__measure',
            'factor__group',
            'measure',
            'measure_value',
            'rationale')
    meeting_items = meeting.meetingitem_set.select_related('decision_item')
    total_items = meeting_items.count()
    search_query = request.GET.get('search')
    if search_query:
        meeting_items = meeting_items.filter(decision_item__name__icontains=search_query)
    return render(request, template_name, {
        'meeting': meeting,
        'factors': factors,
        'measure': measure,
        'measure_values': measure_values,
        'relative_col_size': relative_col_size,
        'evaluations': evaluations,
        'total_items': total_items,
        'meeting_items': meeting_items,
        'search_query': search_query})


@login_required
@require_POST
def save_evaluation(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)

    meeting_item_id = request.POST.get('meeting_item_id')
    factor_id = request.POST.get('factor_id')
    measure_id = request.POST.get('measure_id')
    measure_value_id = request.POST.get('measure_value_id')

    meeting_item = MeetingItem.objects.get(pk=meeting_item_id)
    factor = Factor.objects.get(pk=factor_id)
    measure = Measure.objects.get(pk=measure_id)

    if measure_value_id:
        measure_value = MeasureValue.objects.get(pk=measure_value_id)
    else:
        measure_value = None

    with transaction.atomic():
        Evaluation.objects.update_or_create(
            meeting=meeting,
            meeting_item=meeting_item,
            user=request.user,
            factor=factor,
            measure=measure,
            defaults={'evaluated_at': timezone.now(), 'measure_value': measure_value}
        )

        meeting_item.calculate_ranking()
        for scenario in meeting_item.scenarios.all():
            scenario.calculate_ranking()
        meeting.deliverable.save()
        meeting.calculate_progress()
        meeting_stakeholder, created = MeetingStakeholder.objects.get_or_create(meeting=meeting, stakeholder=request.user)
        meeting_stakeholder.update_meeting_input()

    context = get_meeting_progress(meeting)
    return HttpResponse(json.dumps(context), content_type='application/json')


@login_required
@require_POST
def save_rationale(request, deliverable_id, meeting_id):
    try:
        meeting = Meeting.objects.get(pk=meeting_id, deliverable__id=deliverable_id)

        meeting_item_id = request.POST.get('meeting_item_id')
        factor_id = request.POST.get('factor_id')
        measure_id = request.POST.get('measure_id')

        meeting_item = MeetingItem.objects.get(pk=meeting_item_id)
        factor = Factor.objects.get(pk=factor_id)
        measure = Measure.objects.get(pk=measure_id)

        evaluation, created = Evaluation.objects.get_or_create(
            meeting=meeting,
            user=request.user,
            meeting_item=meeting_item,
            factor=factor,
            measure=measure
        )

        if evaluation.rationale:
            form = RationaleForm(request.POST, instance=evaluation.rationale)
            form.instance.updated_by = request.user
        else:
            form = RationaleForm(request.POST)
            form.instance.created_by = request.user
            form.instance.meeting = meeting

        if form.is_valid():
            evaluation.rationale = form.save()
            if len(evaluation.rationale.text) == 0:
                evaluation.rationale.delete()
                evaluation.rationale = None
            evaluation.save()
            meeting.deliverable.save()
            meeting_item.update_has_rationales()
            meeting.calculate_meeting_related_rationales_count()
            context = get_meeting_progress(meeting)
            return HttpResponse(json.dumps(context), content_type='application/json')
        else:
            return HttpResponseBadRequest(form['text'].errors.as_text())

    except ObjectDoesNotExist:
        return HttpResponseBadRequest(_('An error ocurred while trying to save your data.'))
