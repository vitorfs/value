# coding: utf-8

import xlrd
from string import ascii_uppercase

from django.http import HttpResponse, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.forms.models import modelform_factory, modelformset_factory, inlineformset_factory
from django.db import transaction
from django.db.models.functions import Lower

from value.application_settings.models import ApplicationSetting
from value.factors.models import Factor
from value.measures.models import Measure
from value.deliverables.decorators import user_is_manager, user_is_stakeholder
from value.deliverables.models import Deliverable, DecisionItem, DecisionItemAttachment, DecisionItemLookup
from value.deliverables.meetings.models import Evaluation
from value.deliverables.forms import UploadFileForm, DeliverableForm, DeliverableBasicDataForm, \
        DeliverableFactorsForm, DeliverableMeasureForm
from value.deliverables.utils import excel_column_map


@login_required
def index(request):
    manager_deliverables = Deliverable.objects.filter(manager=request.user).order_by('-updated_at')
    stakeholder_deliverables = Deliverable.objects.filter(stakeholders__in=[request.user]).exclude(manager=request.user).order_by('-updated_at')
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
        messages.warning(request, u'There is not active measure. Please configure it properly on Management » Measures.')

    has_factors = Factor.objects.filter(is_active=True).exists()
    if not has_factors:
        messages.warning(request, u'There is not active value factor. Please configure it properly on Management » Factors.')

    if request.method == 'POST':
        form = DeliverableForm(request.POST)
        formset = DecisionItemFormSet(request.POST, prefix='decision_item')

        if form.is_valid() and formset.is_valid():
            form.instance.manager = request.user
            form.instance.created_by = request.user
            deliverable = form.save()

            for form in formset:
                form.instance.deliverable = deliverable

            formset.save()
            deliverable.save()

            messages.success(request, u'The deliverable {0} was added successfully.'.format(deliverable.name))

            return redirect(reverse('deliverables:deliverable', args=(deliverable.pk,)))
        else:
            messages.error(request, u'Please correct the error below.')
    else:
        form = DeliverableForm(initial={'factors': Factor.objects.filter(is_active=True)})
        formset = DecisionItemFormSet(prefix='decision_item', queryset=DecisionItem.objects.none())
    return render(request, 'deliverables/new.html', { 
            'fields': fields,
            'form': form,
            'formset': formset
            })

@login_required
@require_POST
def import_decision_items(request):
    form = UploadFileForm(request.POST, request.FILES)
    html = ''
    if form.is_valid():
        app_settings = ApplicationSetting.get()
        column_map = excel_column_map()
        f = request.FILES['file']
        filename = f.name
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
        DecisionItemFormSet = modelformset_factory(DecisionItem, fields=fields.keys(), extra=len(decision_items))
        formset = DecisionItemFormSet(prefix='decision_item', queryset=DecisionItem.objects.none(), initial=decision_items)
        html = render_to_string('deliverables/includes/decision_items_import_table.html', {
                'decision_items': decision_items,
                'fields': fields,
                'formset': formset,
                'filename': filename
                })
    return HttpResponse(html)

@login_required
@user_is_stakeholder
def deliverable(request, deliverable_id):
    return redirect(reverse('deliverables:meetings:index', args=(deliverable_id,)))

@login_required
@user_is_stakeholder
def stakeholders(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    return render(request, 'deliverables/stakeholders.html', { 'deliverable': deliverable })

@login_required
@user_is_manager
def load_available_stakeholders(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    available_stakeholders = User.objects.filter(is_active=True).exclude(pk__in=deliverable.get_stakeholders())
    html = render_to_string('deliverables/includes/add_stakeholders.html', { 'available_stakeholders': available_stakeholders })
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
        messages.success(request, u'The stakeholders were added successfully.')
    else:
        messages.warning(request, u'No stakeholder were selected. Nothing changed.')
    return redirect(reverse('deliverables:stakeholders', args=(deliverable.pk,)))

@login_required
@user_is_manager
@require_POST
def remove_stakeholder(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    user_ids = request.POST.getlist('stakeholders')
    users = User.objects.filter(pk__in=user_ids)
    deliverable.stakeholders.remove(*users)
    messages.success(request, u'The stakeholders were removed successfully.')
    return redirect('deliverables:stakeholders', deliverable.pk)

@login_required
@require_POST
def process_decision_items_list_actions(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    action = request.POST.get('action')
    if action == 'delete_selected':
        decision_items_ids = request.POST.getlist('decision_item_id')
        decision_items = DecisionItem.objects.filter(pk__in=decision_items_ids)
        if 'confirm_action' in request.POST:
            decision_items.delete()
            deliverable.save()
            messages.success(request, 'The selected decision items were deleted successfully.')
        else:
            return render(request, 'deliverables/decision_items/delete_list.html', { 
                    'deliverable': deliverable, 
                    'decision_items': decision_items, 
                    'action': action 
                    })
    return redirect(reverse('deliverables:decision_items', args=(deliverable.pk,)))

@login_required
@user_is_stakeholder
def decision_items(request, deliverable_id):
    if request.method == 'POST':
        return process_decision_items_list_actions(request, deliverable_id)
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    return render(request, 'deliverables/decision_items/list.html', { 'deliverable': deliverable })

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
    fields = DecisionItemLookup.get_all_fields()
    DecisionItemForm = modelform_factory(DecisionItem, fields=fields.keys())
    if request.method == 'POST':
        form = DecisionItemForm(request.POST, instance=DecisionItem(deliverable=deliverable))
        if form.is_valid():
            decision_item = form.save()
            deliverable.save()
            messages.success(request, u'The decision item {0} was added successfully.'.format(decision_item.name))
            return redirect(reverse('deliverables:decision_items', args=(deliverable.pk,)))
        else:
            messages.error(request, u'Please correct the error below.')
    else:
        form = DecisionItemForm()
    return render(request, 'deliverables/decision_items/add.html', { 
            'deliverable': deliverable,
            'fields': fields,
            'form': form
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
            messages.success(request, u'The decision item {0} was saved successfully.'.format(decision_item.name))
            return redirect(reverse('deliverables:decision_items', args=(deliverable.pk,)))
        else:
            messages.error(request, u'Please correct the error below.')
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
        messages.success(request, u'The decision item {0} was deleted successfully.'.format(decision_item.name))
        return redirect(reverse('deliverables:decision_items', args=(deliverable.pk,)))
    else:
        related_evaluations = Evaluation.objects.filter(meeting_item__decision_item=decision_item).order_by('meeting')
        return render(request, 'deliverables/decision_items/delete.html', { 
                'deliverable': deliverable,
                'decision_item': decision_item,
                'related_evaluations': related_evaluations
                })

@login_required
@user_is_stakeholder
def details_decision_item(request, deliverable_id, decision_item_id):
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
def settings(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    users = User.objects.exclude(pk=request.user.id).order_by(Lower('first_name').asc(), Lower('last_name').asc(), Lower('username').asc())
    if request.method == 'POST':
        form = DeliverableBasicDataForm(request.POST, instance=deliverable)
        if form.is_valid():
            form.save()
            messages.success(request, u'The deliverable {0} was saved successfully.'.format(deliverable.name))
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
            for meeting in deliverable.meeting_set.all():
                #meeting.evaluation_set.exclude(factor__in=deliverable.factors.all()).delete()
                meeting.calculate_all_rankings()

            messages.success(request, u'The deliverable {0} was saved successfully.'.format(deliverable.name))
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
            for meeting in deliverable.meeting_set.all():
                meeting.calculate_all_rankings()
            messages.success(request, u'The deliverable {0} was saved successfully.'.format(deliverable.name))
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
@transaction.atomic
@require_POST
def delete(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    deliverable.delete()
    messages.success(request, u'The deliverable {0} was completly deleted successfully.'.format(deliverable.name))
    return redirect(reverse('deliverables:index'))

@login_required
@user_is_manager
@require_POST
def transfer(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    try:
        user_id = request.POST.get('user')
        user = User.objects.get(pk=user_id)
        deliverable.stakeholders.add(deliverable.manager)
        deliverable.manager = user
        deliverable.save()
        messages.success(request, u'The deliverable {0} was successfully transferred to {1}.'.format(deliverable.name, user.profile.get_display_name()))
        return redirect(reverse('deliverables:index'))
    except:
        messages.error(request, 'Something went wrong. Nothing changed.')
    return redirect(reverse('deliverables:settings', args=(deliverable.pk,)))

@login_required
def historical_dashboard(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    return render(request, 'deliverables/historical_dashboard.html', { 'deliverable': deliverable })
