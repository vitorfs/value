# coding: utf-8

from collections import OrderedDict

from colour import Color
from jira import JIRA
import xlrd

from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.core.urlresolvers import reverse
from django.conf import settings as django_settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.forms.models import modelform_factory, modelformset_factory, inlineformset_factory
from django.db import transaction
from django.db.models import Count
from django.db.models.functions import Lower
from django.utils.translation import ugettext as _

from value.application_settings.models import ApplicationSetting
from value.factors.models import Factor
from value.measures.models import Measure
from value.deliverables.decorators import user_is_manager, user_is_stakeholder
from value.deliverables.models import Deliverable, DecisionItem, DecisionItemAttachment, DecisionItemLookup
from value.deliverables.meetings.models import Evaluation, Meeting
from value.deliverables.forms import UploadFileForm, DeliverableForm, DeliverableBasicDataForm, \
    DeliverableFactorsForm, DeliverableMeasureForm, DeliverableRemoveStakeholdersForm, JiraSearchIssuesForm, \
    DeliverableAdminsForm
from value.deliverables.utils import excel_column_map


@login_required
def index(request):
    manager_deliverables = Deliverable.objects \
        .filter(manager=request.user) \
        .select_related('manager', 'manager__profile') \
        .prefetch_related('meeting_set', 'stakeholders__profile') \
        .order_by('-updated_at')

    stakeholder_deliverables = Deliverable.objects \
        .filter(stakeholders__in=[request.user]) \
        .exclude(manager=request.user) \
        .select_related('manager', 'manager__profile') \
        .prefetch_related('meeting_set') \
        .order_by('-updated_at')

    return render(request, 'deliverables/index.html', {
        'manager_deliverables': manager_deliverables,
        'stakeholder_deliverables': stakeholder_deliverables
    })


@login_required
@transaction.atomic
def new(request):
    fields = DecisionItemLookup.get_visible_fields()
    DecisionItemFormSet = modelformset_factory(DecisionItem, fields=fields.keys())

    has_measure = Measure.objects.filter(is_active=True).exists()
    if not has_measure:
        messages.warning(
            request,
            _(u'There is not active measure. Please configure it properly on Management » Measures.')
        )

    has_factors = Factor.objects.filter(is_active=True).exists()
    if not has_factors:
        messages.warning(
            request,
            _(u'There is not active value factor. Please configure it properly on Management » Factors.')
        )

    stakeholders_queryset = User.objects.filter(is_active=True) \
        .order_by('first_name', 'last_name', 'username') \
        .exclude(pk=request.user.pk)

    if request.method == 'POST':
        form = DeliverableForm(request.POST)
        form.fields['stakeholders'].queryset = stakeholders_queryset
        formset = DecisionItemFormSet(request.POST, prefix='decision_item')

        if form.is_valid() and formset.is_valid():
            form.instance.manager = request.user
            form.instance.created_by = request.user
            deliverable = form.save()

            for form in formset:
                form.instance.deliverable = deliverable

            formset.save()
            deliverable.save()

            messages.success(request, _(u'The deliverable {0} was added successfully.').format(deliverable.name))
            return redirect(reverse('deliverables:deliverable', args=(deliverable.pk,)))
        else:
            messages.error(request, _(u'Please correct the error below.'))
    else:
        form = DeliverableForm(initial={'factors': Factor.objects.filter(is_active=True)})
        form.fields['stakeholders'].queryset = stakeholders_queryset
        formset = DecisionItemFormSet(prefix='decision_item', queryset=DecisionItem.objects.none())
    return render(request, 'deliverables/new.html', {
        'fields': fields,
        'form': form,
        'formset': formset
    })


@login_required
@require_POST
def import_decision_items(request):
    try:
        form = UploadFileForm(request.POST, request.FILES)
        html = ''
        if form.is_valid():
            app_settings = ApplicationSetting.get()
            column_map = excel_column_map()
            f = request.FILES['file']
            filename = f.name
            if '.xls' in filename or '.xlsx' in filename:
                wb = xlrd.open_workbook(filename=None, file_contents=f.read())
                decision_items = []
                for sheet in wb.sheets():
                    for row in range(app_settings['EXCEL_STARTING_ROW_COLUMN'] - 1, sheet.nrows):
                        decision_item = {}
                        for key in app_settings['EXCEL_IMPORT_TEMPLATE'].keys():
                            column_name = app_settings['EXCEL_IMPORT_TEMPLATE'][key]
                            try:
                                decision_item[key] = sheet.cell(row, column_map[column_name]).value
                            except:
                                pass
                        decision_items.append(decision_item)
                fields = DecisionItemLookup.get_visible_fields()
                DecisionItemFormSet = modelformset_factory(
                    DecisionItem,
                    fields=fields.keys(),
                    extra=len(decision_items)
                )
                formset = DecisionItemFormSet(
                    prefix='decision_item',
                    queryset=DecisionItem.objects.none(),
                    initial=decision_items
                )
                html = render_to_string('deliverables/includes/decision_items_import_table.html', {
                    'decision_items': decision_items,
                    'fields': fields,
                    'formset': formset,
                    'filename': filename
                })
                return HttpResponse(html)
            else:
                return HttpResponseBadRequest(_('Invalid file type. Supported extensions are .xls or .xlsx'))
        return HttpResponseBadRequest(_('Invalid form data.'))
    except:
        return HttpResponseBadRequest(_('An unexpected error ocurred.'))


@login_required
@user_is_stakeholder
def deliverable(request, deliverable_id):
    return redirect(reverse('deliverables:meetings:index', args=(deliverable_id,)))


@login_required
@user_is_stakeholder
def stakeholders(request, deliverable_id):
    try:
        deliverable = Deliverable.objects \
            .select_related('manager__profile') \
            .prefetch_related('stakeholders__profile', 'stakeholders__groups', 'manager__groups') \
            .get(pk=deliverable_id)
    except Deliverable.DoesNotExist:
        raise Http404
    return render(request, 'deliverables/stakeholders.html', {'deliverable': deliverable})


@login_required
@user_is_manager
def load_available_stakeholders(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    available_stakeholders = User.objects.filter(is_active=True).exclude(pk__in=deliverable.get_all_stakeholders())
    html = render_to_string('deliverables/includes/add_stakeholders.html', {
        'available_stakeholders': available_stakeholders
    })
    return HttpResponse(html)


@login_required
@user_is_manager
@require_POST
def add_stakeholders(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    user_ids = request.POST.getlist('stakeholders')
    if user_ids:
        for user_id in user_ids:
            stakeholder = User.objects.get(pk=user_id)
            deliverable.stakeholders.add(stakeholder)
        deliverable.save()
        messages.success(request, _(u'The stakeholders were added successfully.'))
    else:
        messages.warning(request, _(u'No stakeholder were selected. Nothing changed.'))
    return redirect(reverse('deliverables:stakeholders', args=(deliverable.pk,)))


@login_required
@user_is_manager
@transaction.atomic
@require_POST
def remove_stakeholder(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    form = DeliverableRemoveStakeholdersForm(request.POST)
    if form.is_valid():
        users = form.cleaned_data['stakeholders']
        deliverable.stakeholders.remove(*users)
        messages.success(request, _(u'The stakeholders were removed successfully.'))
    else:
        messages.error(request, _('An error ocurred while trying to remove the selected stakeholders.'))
    return redirect('deliverables:stakeholders', deliverable.pk)


@login_required
@require_POST
def process_decision_items_list_actions(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    action = request.POST.get('action')
    if action == 'delete_selected':
        decision_items_ids = request.POST.getlist('decision_item_id')
        decision_items = DecisionItem.objects.filter(pk__in=decision_items_ids)

        decision_items_list = {'can_delete': list(), 'cannot_delete': list()}
        decision_items_list['can_delete'] = filter(lambda i: not i.meetingitem_set.exists(), decision_items)
        decision_items_list['cannot_delete'] = filter(lambda i: i.meetingitem_set.exists(), decision_items)

        if 'confirm_action' in request.POST:
            for decision_item in decision_items:
                if not decision_item.meetingitem_set.exists():
                    decision_item.delete()
            deliverable.save()
            messages.success(request, _('The selected decision items were deleted successfully.'))
        else:
            return render(request, 'deliverables/decision_items/delete_list.html', {
                'deliverable': deliverable,
                'decision_items': decision_items_list,
                'action': action
            })
    return redirect(reverse('deliverables:decision_items', args=(deliverable.pk,)))


@login_required
@user_is_stakeholder
def decision_items(request, deliverable_id):
    if request.method == 'POST':
        return process_decision_items_list_actions(request, deliverable_id)
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    return render(request, 'deliverables/decision_items/list.html', {'deliverable': deliverable})


@login_required
@user_is_manager
@require_POST
def save_imported_decision_items(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    fields = DecisionItemLookup.get_all_fields()
    DecisionItemFormSet = modelformset_factory(DecisionItem, fields=fields.keys())
    formset = DecisionItemFormSet(request.POST, prefix='decision_item')
    if formset.is_valid():
        for form in formset:
            form.instance.deliverable = deliverable
        formset.save()
        deliverable.save()
        html = render_to_string('deliverables/decision_items/includes/decision_items_table.html', {
            'deliverable': deliverable
        })
        return HttpResponse(html)
    else:
        html = render_to_string('deliverables/includes/decision_items_import_table.html', {
            'fields': fields,
            'formset': formset
        })
        return HttpResponseBadRequest(html)


@login_required
@user_is_manager
def add_decision_item(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    decision_item = DecisionItem(deliverable=deliverable)
    fields = DecisionItemLookup.get_all_fields()
    DecisionItemForm = modelform_factory(DecisionItem, fields=fields.keys())
    AttachmentFormset = inlineformset_factory(DecisionItem, DecisionItemAttachment, fields=('attachment',))
    if request.method == 'POST':
        form = DecisionItemForm(request.POST, instance=decision_item)
        formset = AttachmentFormset(request.POST, request.FILES, instance=decision_item)
        if form.is_valid() and formset.is_valid():
            decision_item = form.save()
            for form in formset:
                if form.is_valid() and form.instance.attachment:
                    form.instance.decision_item = decision_item
                    form.save()
            formset.save()
            deliverable.save()
            messages.success(request, _(u'The decision item {0} was added successfully.').format(decision_item.name))
            return redirect(reverse('deliverables:decision_items', args=(deliverable.pk,)))
        else:
            messages.error(request, _(u'Please correct the error below.'))
    else:
        form = DecisionItemForm()
        formset = AttachmentFormset(instance=decision_item)
    return render(request, 'deliverables/decision_items/add.html', {
        'deliverable': deliverable,
        'fields': fields,
        'form': form,
        'formset': formset
    })


@login_required
@user_is_manager
def edit_decision_item(request, deliverable_id, decision_item_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    decision_item = get_object_or_404(DecisionItem, pk=decision_item_id)
    fields = DecisionItemLookup.get_all_fields()
    DecisionItemForm = modelform_factory(DecisionItem, fields=fields.keys())
    AttachmentFormset = inlineformset_factory(DecisionItem, DecisionItemAttachment, fields=('attachment',))
    if request.method == 'POST':
        form = DecisionItemForm(request.POST, instance=decision_item)
        formset = AttachmentFormset(request.POST, request.FILES, instance=decision_item)
        if form.is_valid() and formset.is_valid():
            decision_item = form.save()
            for form in formset:
                if form.is_valid() and form.instance.attachment:
                    form.save()
            formset.save()
            deliverable.save()
            messages.success(request, _(u'The decision item {0} was saved successfully.').format(decision_item.name))
            return redirect(reverse('deliverables:decision_items', args=(deliverable.pk,)))
        else:
            messages.error(request, _(u'Please correct the error below.'))
    else:
        form = DecisionItemForm(instance=decision_item)
        formset = AttachmentFormset(instance=decision_item)
    return render(request, 'deliverables/decision_items/edit.html', {
        'deliverable': deliverable,
        'fields': fields,
        'form': form,
        'formset': formset
    })


@login_required
@user_is_manager
def delete_decision_item(request, deliverable_id, decision_item_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    decision_item = get_object_or_404(DecisionItem, pk=decision_item_id)
    if request.method == 'POST':
        decision_item.delete()
        deliverable.save()
        messages.success(request, _(u'The decision item {0} was deleted successfully.').format(decision_item.name))
        return redirect(reverse('deliverables:decision_items', args=(deliverable.pk,)))
    else:
        related_evaluations = Evaluation.objects.filter(meeting_item__decision_item=decision_item).order_by('meeting')
        return render(request, 'deliverables/decision_items/delete.html', {
            'deliverable': deliverable,
            'decision_item': decision_item,
            'related_evaluations': related_evaluations
        })


@login_required
def details_decision_item(request, deliverable_id, decision_item_id):
    '''
    TODO: protected this view again with `user_is_stakeholder`
    The decorator was removed temporarely due to the Survey update
    '''
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    decision_item = get_object_or_404(DecisionItem, pk=decision_item_id)
    fields = DecisionItemLookup.get_all_fields()
    return render(request, 'deliverables/decision_items/includes/decision_item_details.html', {
        'deliverable': deliverable,
        'item': decision_item,
        'fields': fields
    })


@login_required
@user_is_manager
def jira_search_issues(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)

    try:
        jira = JIRA(
            server=django_settings.JIRA_URL,
            basic_auth=(django_settings.JIRA_USERNAME, django_settings.JIRA_PASSWORD)
        )
    except:
        messages.error(request, _('It was not possible to connect to the JIRA server. Either the JIRA credentials are wrong or misconfigurated. Please contact the server administrator.'))
        return redirect('deliverables:decision_items', deliverable_id)

    issues = list()

    if request.method == 'POST':
        form = JiraSearchIssuesForm(request.POST, jira=jira)
        if form.is_valid():
            issues = form.issues
    else:
        form = JiraSearchIssuesForm()

    return render(request, 'deliverables/decision_items/jira_search_issues.html', {
        'deliverable': deliverable,
        'form': form,
        'issues': issues
    })


@login_required
@user_is_manager
@require_POST
def jira_import_issues(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)

    try:
        jira = JIRA(
            server=django_settings.JIRA_URL,
            basic_auth=(django_settings.JIRA_USERNAME, django_settings.JIRA_PASSWORD)
        )
    except:
        messages.error(request, _('It was not possible to connect to the JIRA server. Either the JIRA credentials are wrong or misconfigurated. Please contact the server administrator.'))
        return redirect('deliverables:decision_items', deliverable_id)

    count = 0
    for key in request.POST.getlist('issues'):
        issue = jira.issue(key, fields='summary')
        item, created = DecisionItem.objects.update_or_create(
            deliverable=deliverable,
            name=key,
            is_managed=True,
            defaults={
                'description': issue.fields.summary,
                'column_1': issue.permalink()
            }
        )
        if created:
            count += 1
    if count > 0:
        messages.success(request, _(u'{0} new item(s) imported from JIRA.').format(count))
    else:
        messages.warning(request, _(u'No items imported from JIRA.'))
    return redirect('deliverables:decision_items', deliverable.pk)


@login_required
@user_is_manager
def settings(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    users = User.objects \
        .exclude(pk=request.user.id) \
        .select_related('profile') \
        .order_by(
            Lower('first_name').asc(),
            Lower('last_name').asc(),
            Lower('username').asc()
        )
    if request.method == 'POST':
        form = DeliverableBasicDataForm(request.POST, instance=deliverable)
        if form.is_valid():
            form.save()
            messages.success(request, _(u'The deliverable {0} was saved successfully.').format(deliverable.name))
            # redirect after post to avoid form re-submition
            return redirect(reverse('deliverables:settings', args=(deliverable.pk,)))
    else:
        form = DeliverableBasicDataForm(instance=deliverable)
    return render(request, 'deliverables/settings/details.html', {
        'deliverable': deliverable,
        'form': form,
        'users': users
    })


@login_required
@user_is_manager
def factors_settings(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    if request.method == 'POST':
        form = DeliverableFactorsForm(request.POST, instance=deliverable)
        if form.is_valid():
            deliverable = form.save()
            messages.success(request, _(u'The deliverable {0} was saved successfully.').format(deliverable.name))
            # redirect after post to avoid form re-submition
            return redirect(reverse('deliverables:factors_settings', args=(deliverable.pk,)))
    else:
        form = DeliverableFactorsForm(instance=deliverable)
    return render(request, 'deliverables/settings/factors.html', {
        'deliverable': deliverable,
        'form': form
    })


@login_required
@user_is_manager
def measure_settings(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    if request.method == 'POST':
        form = DeliverableMeasureForm(request.POST, instance=deliverable)
        if form.is_valid():
            deliverable = form.save()
            messages.success(request, _(u'The deliverable {0} was saved successfully.').format(deliverable.name))
            # redirect after post to avoid form re-submition
            return redirect(reverse('deliverables:measure_settings', args=(deliverable.pk,)))
    else:
        form = DeliverableMeasureForm(instance=deliverable)

    return render(request, 'deliverables/settings/measure.html', {
        'deliverable': deliverable,
        'form': form
    })


@login_required
@user_is_manager
def access_settings(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    if request.method == 'POST':
        form = DeliverableAdminsForm(request.POST, instance=deliverable)
        if form.is_valid():
            deliverable = form.save()
            messages.success(request, _(u'The deliverable {0} was saved successfully.').format(deliverable.name))
            # redirect after post to avoid form re-submition
            return redirect(reverse('deliverables:access_settings', args=(deliverable.pk,)))
    else:
        form = DeliverableAdminsForm(instance=deliverable)

    return render(request, 'deliverables/settings/access.html', {
        'deliverable': deliverable,
        'form': form
    })


@login_required
@user_is_manager
@transaction.atomic
@require_POST
def transfer(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    try:
        user_id = request.POST.get('user')
        user = User.objects.get(pk=user_id)
        deliverable.stakeholders.add(deliverable.manager)
        deliverable.stakeholders.remove(user)
        deliverable.manager = user
        deliverable.save()
        messages.success(request, _(u'The deliverable {0} was successfully transferred to {1}.').format(
            deliverable.name,
            user.profile.get_display_name())
        )
        return redirect(reverse('deliverables:index'))
    except:
        messages.error(request, _('Something went wrong. Nothing changed.'))
    return redirect(reverse('deliverables:settings', args=(deliverable.pk,)))


@login_required
@user_is_stakeholder
def historical_dashboard(request, deliverable_id):
    try:
        deliverable = Deliverable.objects \
            .select_related('manager') \
            .get(pk=deliverable_id)
    except Deliverable.DoesNotExist:
        raise Http404

    meetings = deliverable.meeting_set \
        .annotate(items_count=Count('meetingitem', distinct=True)) \
        .annotate(stakeholders_count=Count('meetingstakeholder', distinct=True)) \
        .select_related('deliverable') \
        .all() \
        .order_by('created_at')
    decision_items = deliverable.decisionitem_set \
        .prefetch_related('meetingitem_set__meeting', 'meetingitem_set__evaluation_summary__measure_value') \
        .all() \
        .order_by(Lower('name'))

    for decision_item in decision_items:
        item_meetings = dict()
        for meeting in meetings:
            item_meetings[meeting.pk] = None
        for item in decision_item.meetingitem_set.all():
            item_meetings[item.meeting.pk] = item
        # Put the meeting items in the correct order
        item_meetings = OrderedDict(sorted(item_meetings.items()))

        # Calculate the value ranking variation
        previous_item = None
        for meeting, item in item_meetings.iteritems():
            if item is not None:
                if previous_item is not None:
                    variance = item.value_ranking - previous_item.value_ranking
                else:
                    variance = 0
                item.variance = round(variance, 2)
                previous_item = item

        decision_item.meetings = item_meetings

    return render(request, 'deliverables/historical_dashboard/summary.html', {
        'deliverable': deliverable,
        'meetings': meetings,
        'decision_items': decision_items
    })


@login_required
@user_is_stakeholder
def historical_dashboard_progress(request, deliverable_id):
    try:
        deliverable = Deliverable.objects \
            .select_related('manager') \
            .get(pk=deliverable_id)
    except Deliverable.DoesNotExist:
        raise Http404

    decision_item_id = request.GET.get('id', None)
    if decision_item_id:
        try:
            chart_item = deliverable.decisionitem_set.get(pk=decision_item_id)
        except DecisionItem.DoesNotExist:
            return redirect(reverse('deliverables:historical_dashboard_progress', args=(deliverable.pk, )))
    else:
        chart_item = deliverable.decisionitem_set.all().order_by(Lower('name')).first()

    meeting_items = chart_item.meetingitem_set.order_by('meeting__created_at').select_related('meeting')
    decision_items = deliverable \
        .decisionitem_set \
        .all() \
        .annotate(items_count=Count('meetingitem')) \
        .order_by(Lower('name'))

    return render(request, 'deliverables/historical_dashboard/decision_items_progress.html', {
        'deliverable': deliverable,
        'meeting_items': meeting_items,
        'decision_items': decision_items,
        'chart_item': chart_item
    })


@login_required
@user_is_stakeholder
def historical_dashboard_meeting(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    items = meeting.meetingitem_set.all().order_by('-meeting_decision', '-meeting_ranking', '-value_ranking')

    green_count = items.filter(meeting_decision=True).count()
    if green_count > 5:
        strong_green = Color('#166006')
        light_green = Color('#a0dc93')
    else:
        strong_green = Color('#30841e')
        light_green = Color('#71c060')

    red_count = items.filter(meeting_decision=False).count()
    if red_count > 5:
        light_red = Color('#ff9081')
        strong_red = Color('#891000')
    else:
        light_red = Color('#cf5140')
        strong_red = Color('#901909')

    if green_count > 0:
        green_gradient = strong_green.range_to(light_green, green_count)
        green_colors = list(green_gradient)
    else:
        green_colors = list()

    if red_count > 0:
        red_gradient = light_red.range_to(strong_red, red_count)
        red_colors = list(red_gradient)
    else:
        red_colors = list()

    green_index = 0
    red_index = 0
    for item in items:
        if item.meeting_decision:
            color = green_colors[green_index]
            item.background_color = color.get_hex()
            item.color = '#fff'
            green_index += 1
        else:
            color = red_colors[red_index]
            item.background_color = color.get_hex()
            item.color = '#fff'
            red_index += 1

    return render(request, 'deliverables/historical_dashboard/includes/partial_meeting.html', {
        'meeting': meeting,
        'items': items
    })
