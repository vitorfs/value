import xlrd
from string import ascii_uppercase

from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.forms.models import modelform_factory, modelformset_factory
from django.db import transaction

from value.deliverables.models import Deliverable, DecisionItem, DecisionItemLookup
from value.deliverables.meetings.models import Evaluation
from value.deliverables.forms import UploadFileForm, DeliverableForm
from value.application_settings.models import ApplicationSetting


@login_required
def index(request):
    deliverables = Deliverable.objects.all().order_by('-updated_at')
    return render(request, 'deliverables/index.html', { 'deliverables': deliverables })

@login_required
@user_passes_test(lambda user: user.is_superuser)
@transaction.atomic
def new(request):
    fields = DecisionItemLookup.get_all_fields()
    DecisionItemFormSet = modelformset_factory(DecisionItem, fields=fields.keys())

    if request.method == 'POST':
        form = DeliverableForm(request.POST)
        formset = DecisionItemFormSet(request.POST, prefix='decision_item')

        if form.is_valid() and formset.is_valid():
            form.instance.manager = request.user
            form.instance.created_by = request.user
            deliverable = form.save()

            for form in formset:
                form.instance.deliverable = deliverable
                form.instance.created_by = request.user

            formset.save()
            deliverable.save()

            messages.success(request, u'The deliverable {0} was added successfully.'.format(deliverable.name))

            return redirect(reverse('deliverables:index'))
        else:
            messages.error(request, u'Please correct the error below.')
    else:
        form = DeliverableForm()
        formset = DecisionItemFormSet(prefix='decision_item', queryset=DecisionItem.objects.none())
    return render(request, 'deliverables/new.html', { 
            'fields': fields,
            'form': form,
            'formset': formset
            })

def _excel_column_map():
    column_map = {}
    i = 0
    for c in ascii_uppercase:
        column_map[c] = i
        i = i + 1
    for c in ascii_uppercase:
        c = 'A{0}'.format(c)
        column_map[c] = i
        i = i + 1
    for c in ascii_uppercase:
        c = 'B{0}'.format(c)
        column_map[c] = i
        i = i + 1
    return column_map

@login_required
@user_passes_test(lambda user: user.is_superuser)
@require_POST
def import_decision_items(request):
    form = UploadFileForm(request.POST, request.FILES)
    html = ''
    if form.is_valid():
        app_settings = ApplicationSetting.get()
        column_map = _excel_column_map()
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
        fields = DecisionItemLookup.get_all_fields()
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
def deliverable(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    return render(request, 'deliverables/deliverable.html', { 'deliverable': deliverable })

@login_required
def stakeholders(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    return render(request, 'deliverables/stakeholders.html', { 'deliverable': deliverable })

@login_required
def load_available_stakeholders(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    available_stakeholders = User.objects.filter(is_active=True).exclude(pk__in=deliverable.stakeholders.all())
    html = render_to_string('deliverables/includes/add_stakeholders.html', { 'available_stakeholders': available_stakeholders })
    return HttpResponse(html)

@login_required
@user_passes_test(lambda user: user.is_superuser)
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
@user_passes_test(lambda user: user.is_superuser)
@require_POST
def remove_stakeholder(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    user_id = request.POST.get('user_id')
    user = User.objects.get(pk=user_id)
    deliverable.stakeholders.remove(user)
    return HttpResponse(u'{0} was removed successfully.'.format(user.profile.get_display_name()))

@login_required
def decision_items(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    return render(request, 'deliverables/decision_items/list.html', { 'deliverable': deliverable })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def add_decision_item(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    fields = DecisionItemLookup.get_all_fields()
    DecisionItemForm = modelform_factory(DecisionItem, fields=fields.keys())
    if request.method == 'POST':
        form = DecisionItemForm(request.POST, instance=DecisionItem(deliverable=deliverable, created_by=request.user))
        if form.is_valid():
            decision_item = form.save()
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
@user_passes_test(lambda user: user.is_superuser)
def edit_decision_item(request, deliverable_id, decision_item_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    decision_item = get_object_or_404(DecisionItem, pk=decision_item_id)
    fields = DecisionItemLookup.get_all_fields()
    DecisionItemForm = modelform_factory(DecisionItem, fields=fields.keys())
    if request.method == 'POST':
        form = DecisionItemForm(request.POST, instance=decision_item)
        if form.is_valid():
            form.instance.updated_by = request.user
            decision_item = form.save()
            messages.success(request, u'The decision item {0} was saved successfully.'.format(decision_item.name))
            return redirect(reverse('deliverables:decision_items', args=(deliverable.pk,)))
        else:
            messages.error(request, u'Please correct the error below.')
    else:
        form = DecisionItemForm(instance=decision_item)
    return render(request, 'deliverables/decision_items/edit.html', { 
            'deliverable': deliverable,
            'fields': fields,
            'form': form
            })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def delete_decision_item(request, deliverable_id, decision_item_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    decision_item = get_object_or_404(DecisionItem, pk=decision_item_id)
    if request.method == 'POST':
        decision_item.delete()
        messages.success(request, u'The decision item {0} was deleted successfully.'.format(decision_item.name))
        return redirect(reverse('deliverables:decision_items', args=(deliverable.pk,)))
    else:
        related_evaluations = Evaluation.objects.filter(meeting_item__decision_item=decision_item).order_by('meeting')
        return render(request, 'deliverables/decision_items/delete.html', { 
                'deliverable': deliverable,
                'decision_item': decision_item,
                'related_evaluations': related_evaluations
                })
