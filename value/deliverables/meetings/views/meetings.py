# coding: utf-8
import csv
import json

from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q, Count, Case, Value, When, BooleanField
from django.db import transaction
from django.utils import timezone
from django.utils.html import mark_safe
from django.utils.translation import ugettext as _

from value.application_settings.models import ApplicationSetting
from value.deliverables.models import Deliverable, DecisionItemLookup, DecisionItem
from value.deliverables.decorators import user_is_manager, user_is_stakeholder
from value.deliverables.meetings.models import Meeting, MeetingItem, MeetingStakeholder
from value.deliverables.meetings.forms import NewMeetingForm, MeetingForm, MeetingStatusForm, AddStakeholdersForm
from value.deliverables.meetings.utils import get_meeting_progress


@login_required
@user_is_stakeholder
def index(request, deliverable_id):
    try:
        deliverable = Deliverable.objects.select_related('manager__profile').get(pk=deliverable_id)
    except Deliverable.DoesNotExist:
        raise Http404
    return render(request, 'deliverables/meetings.html', {'deliverable': deliverable})


@login_required
@user_is_manager
@transaction.atomic
def new(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    decision_items_fields = DecisionItemLookup.get_visible_fields()

    decision_items = deliverable.decisionitem_set.all() \
        .annotate(meeting_count=Count('meetingitem')) \
        .annotate(
            is_new=Case(
                When(meeting_count=0, then=Value(True)),
                When(meeting_count__gt=0, then=Value(False)),
                default=Value(True),
                output_field=BooleanField(),
            )
        ).order_by('-is_new', 'name',)

    meeting = Meeting(deliverable=deliverable)
    if request.method == 'POST':
        form = NewMeetingForm(request.POST, instance=meeting)
        stakeholder_ids = request.POST.getlist('stakeholders')
        selected_stakeholders = User.objects.filter(id__in=stakeholder_ids)
        meeting_stakeholders = User.objects.filter(
            Q(id__in=selected_stakeholders) | Q(id__in=deliverable.stakeholders.all())
        ).filter(is_active=True).distinct()

        decision_item_ids = request.POST.getlist('decision_item')
        selected_decision_items = deliverable.decisionitem_set.filter(id__in=decision_item_ids)

        if form.is_valid() and selected_stakeholders.exists() and selected_decision_items.exists():
            meeting = form.save(commit=False)
            meeting.deliverable = deliverable
            meeting.measure = deliverable.measure
            meeting.created_by = request.user
            meeting.save()

            meeting.factors = deliverable.factors.filter(is_active=True)

            MeetingStakeholder.objects.create(meeting=meeting, stakeholder=request.user)

            for stakeholder in selected_stakeholders:
                MeetingStakeholder.objects.create(meeting=meeting, stakeholder=stakeholder)

            for decision_item in selected_decision_items:
                MeetingItem.objects.create(meeting=meeting, decision_item=decision_item)

            deliverable.save()

            initial_measure_value = form.cleaned_data.get('default_evaluation')
            if initial_measure_value:
                meeting.initial_data(initial_measure_value)

            retrieve_evaluations = form.cleaned_data.get('retrieve_evaluations', False)
            if retrieve_evaluations:
                meeting.load_past_meeting_evaluations()

            messages.success(request, _(u'The meeting {0} was created successfully.').format(meeting.name))
            return redirect(reverse('deliverables:meetings:meeting', args=(deliverable.pk, meeting.pk,)))
        else:
            messages.error(request, _(u'Please correct the error below.'))
    else:
        form = NewMeetingForm(instance=meeting, initial={'started_at': timezone.now()})
        meeting_stakeholders = deliverable.stakeholders \
            .filter(is_active=True) \
            .order_by('first_name', 'last_name', 'username')
        selected_stakeholders = meeting_stakeholders
        selected_decision_items = decision_items.filter(is_new=True)
    available_stakeholders = User.objects \
        .exclude(id__in=deliverable.stakeholders.all()) \
        .exclude(id__in=selected_stakeholders) \
        .filter(is_active=True) \
        .order_by('first_name', 'last_name', 'username')
    return render(request, 'meetings/new.html', {
        'deliverable': deliverable,
        'decision_items_fields': decision_items_fields,
        'decision_items': decision_items,
        'selected_decision_items': selected_decision_items,
        'form': form,
        'meeting_stakeholders': meeting_stakeholders,
        'available_stakeholders': available_stakeholders,
        'selected_stakeholders': selected_stakeholders
    })


@login_required
def meeting(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    if meeting.status == Meeting.CLOSED:
        return redirect(reverse('deliverables:meetings:final_decision', args=(deliverable_id, meeting_id)))
    elif meeting.status == Meeting.ANALYSING:
        return redirect(reverse('deliverables:meetings:dashboard', args=(deliverable_id, meeting_id)))
    else:
        return redirect(reverse('deliverables:meetings:evaluate', args=(deliverable_id, meeting_id)))


@login_required
@user_is_manager
@require_POST
def change_meeting_status(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    old_status = meeting.get_status_display()
    form = MeetingStatusForm(request.POST, instance=meeting)
    if form.is_valid():
        meeting = form.save()
        meeting.deliverable.save()
        new_status = meeting.get_status_display()
        messages.success(request, _(u'The meeting status was changed from {0} to {1}.').format(old_status, new_status))
    else:
        messages.error(request, _(u'An error ocurred while trying to change meeting status.').format(meeting.name))
    redirect_to = request.POST.get(
        'next',
        reverse('deliverables:meetings:meeting', args=(meeting.deliverable.pk, meeting.pk))
    )
    return redirect(redirect_to)


@login_required
def update_meeting_progress(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    context = get_meeting_progress(meeting)
    return HttpResponse(json.dumps(context), content_type='application/json')


@login_required
def sync_jira(request, deliverable_id, meeting_id):
    try:
        meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
        app_settings = ApplicationSetting.get()
        jira_is_enabled = app_settings.get(ApplicationSetting.JIRA_INTEGRATION_FLAG)
        if jira_is_enabled:
            meeting.update_managed_items(request)
        return HttpResponse()
    except Exception, e:
        return HttpResponseBadRequest(e.text)


@login_required
@require_POST
def remove_stakeholder(request, deliverable_id, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id, deliverable__id=deliverable_id)
    stakeholder_id = request.POST.get('stakeholder')
    user = User.objects.get(pk=stakeholder_id)
    if user != request.user:
        meeting_stakeholder = MeetingStakeholder.objects.get(stakeholder=user, meeting=meeting)
        if meeting_stakeholder.stakeholder.evaluation_set.filter(meeting=meeting).exists():
            messages.warning(
                request,
                _(u'''The stakeholder {0} cannot be removed from this meeting
                because he has already provided evaluation input.''').format(user.profile.get_display_name())
            )
        else:
            meeting_stakeholder.delete()
            meeting.calculate_progress()
            meeting.calculate_all_rankings()
            messages.success(
                request,
                _(u'{0} was successfully removed from the meeting!').format(user.profile.get_display_name())
            )
    else:
        messages.warning(request, _('You cannot remove yourself from the meeting.'))
    return redirect(reverse('deliverables:meetings:stakeholders', args=(deliverable_id, meeting_id)))


@login_required
@require_POST
@transaction.atomic
def add_stakeholders(request, deliverable_id, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id, deliverable__id=deliverable_id)
    form = AddStakeholdersForm(data=request.POST, meeting=meeting)
    if form.is_valid():
        form.add_stakeholders()
        messages.success(request, _(u'Stakeholders sucessfully added to the meeting!'))
    else:
        messages.warning(request, _(u'Select at least one stakeholder to add.'))
    return redirect(reverse('deliverables:meetings:stakeholders', args=(deliverable_id, meeting_id)))


@login_required
@require_POST
@transaction.atomic
def remove_decision_items(request, deliverable_id, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id, deliverable__id=deliverable_id)
    meeting_items_ids = request.POST.getlist('meeting_items')
    if any(meeting_items_ids):
        items = meeting.meetingitem_set.filter(id__in=meeting_items_ids)
        can_delete = filter(lambda i: not i.evaluation_set.exists(), items)
        cannot_delete = filter(lambda i: i.evaluation_set.exists(), items)
        if can_delete:
            for item in can_delete:
                item.delete()
            meeting.calculate_progress()
            meeting.calculate_all_rankings()
            pretty_names = map(lambda i: u'<strong>{0}</strong>'.format(i.decision_item.name), can_delete)
            messages.success(
                request,
                mark_safe(
                    u'{0}<ul><li>{1}</li></ul>'.format(
                        _('The following decision items was sucessfully removed from the meeting:'),
                        u'</li><li>'.join(pretty_names)
                    )
                )
            )
        if cannot_delete:
            pretty_names = map(lambda i: u'<strong>{0}</strong>'.format(i.decision_item.name), cannot_delete)
            messages.warning(
                request,
                mark_safe(
                    u'{0}<ul><li>{1}</li></ul>'.format(
                        _('''The following decision items wasn\'t removed from the meeting because
                        they were already in use:'''),
                        u'</li><li>'.join(pretty_names)
                    )
                )
            )
    else:
        messages.warning(request, _(u'Select at least one decision item to remove.'))
    return redirect(reverse('deliverables:meetings:decision_items', args=(deliverable_id, meeting_id)))


@login_required
@require_POST
@transaction.atomic
def add_decision_items(request, deliverable_id, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id, deliverable__id=deliverable_id)
    decision_items_ids = request.POST.getlist('decision_items')
    if any(decision_items_ids):
        for decision_item_id in decision_items_ids:
            decision_item = DecisionItem.objects.get(pk=decision_item_id)
            meeting_item = MeetingItem(meeting=meeting, decision_item=decision_item)
            meeting_item.save()
        meeting.calculate_progress()
        meeting.calculate_all_rankings()
        messages.success(request, _(u'Decision items sucessfully added to the meeting!'))
    else:
        messages.warning(request, _(u'Select at least one decision item to add.'))
    return redirect(reverse('deliverables:meetings:decision_items', args=(deliverable_id, meeting_id)))


@login_required
def settings(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    survey_url = request.build_absolute_uri(reverse('survey', args=(meeting.survey_id, )))
    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            meeting.deliverable.save()
            messages.success(request, _(u'The meeting details was saved successfully!'))
        else:
            messages.error(request, _(u'Please correct the error below.'))
    else:
        form = MeetingForm(instance=meeting)
    return render(request, 'meetings/settings/details.html', {
        'meeting': meeting,
        'form': form,
        'survey_url': survey_url
    })


@login_required
@user_is_manager
def decision_items(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    decision_items_in_use = meeting.meetingitem_set.values('decision_item__id')
    available_decision_items = meeting.deliverable.decisionitem_set.exclude(id__in=decision_items_in_use)
    return render(request, 'meetings/settings/items.html', {
        'meeting': meeting,
        'available_decision_items': available_decision_items})


@login_required
@user_is_manager
def stakeholders(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    stakeholders = meeting.meetingstakeholder_set.select_related('stakeholder', 'stakeholder__profile')
    available_stakeholders = User.objects \
        .exclude(id__in=meeting.meetingstakeholder_set.values('stakeholder__id')) \
        .filter(is_active=True) \
        .order_by('first_name', 'last_name', 'username')
    return render(request, 'meetings/settings/stakeholders.html', {
        'meeting': meeting,
        'stakeholders': stakeholders,
        'available_stakeholders': available_stakeholders})


@login_required
@require_POST
def remove_idle_stakeholders(request, deliverable_id, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id, deliverable__id=deliverable_id)
    queryset = meeting.meetingstakeholder_set.filter(meeting_input=0.0)
    if queryset.exists():
        queryset.delete()
        meeting.calculate_progress()
        meeting.calculate_all_rankings()
        messages.success(request, _('Stakeholders without input removed with success.'))
    else:
        messages.warning(request, _('There was no stakeholder without input.'))
    return redirect(reverse('deliverables:meetings:stakeholders', args=(deliverable_id, meeting_id)))


@login_required
@user_is_manager
def delete(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    can_delete = (not meeting.evaluation_set.exists())
    if request.method == 'POST' and can_delete:
        meeting.delete()
        messages.success(request, _(u'The meeeting {0} was completly deleted successfully.').format(meeting.name))
        return redirect(reverse('deliverables:deliverable', args=(meeting.deliverable.pk,)))
    return render(request, 'meetings/settings/delete.html', {'meeting': meeting, 'can_delete': can_delete})


@login_required
def export_excel(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)

    evaluations = meeting.get_evaluations() \
        .select_related('meeting_item', 'user', 'factor', 'measure_value', 'rationale') \
        .values_list('user__username', 'user__email', 'meeting_item__decision_item__name',
                     'factor__name', 'measure_value__description', 'rationale__text') \
        .order_by('user', 'meeting_item', 'factor')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    writer = csv.writer(response)
    writer.writerow(['Username', 'Email', 'Item', 'Factor', 'Evaluation', 'Comments'])
    for e in evaluations:
        try:
            row = list()
            for s in e:
                if s is not None:
                    row.append(s.encode('utf-8'))
                else:
                    row.append('')
            writer.writerow(row)
        except Exception, err:
            writer.writerow(['error!'])
    return response
