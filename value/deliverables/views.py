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
from django.forms.models import modelformset_factory
from django.db import transaction

from value.deliverables.models import Deliverable, DecisionItem, DecisionItemLookup
from value.deliverables.forms import UploadFileForm, DeliverableForm
from value.application_settings.models import ApplicationSetting


@login_required
def index(request):
    deliverables = Deliverable.objects.all().order_by('-updated_at')
    return render(request, 'deliverables/index.html', { 'deliverables' : deliverables })

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
            deliverable = form.save(commit=False)

            users_id = request.POST.getlist('stakeholders')
            deliverable.stakeholders = User.objects.filter(pk__in=users_id)
            deliverable.stakeholders.add(request.user)

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
    users = User.objects.filter(is_active=True).exclude(pk=request.user.pk)
    return render(request, 'deliverables/new.html', { 
        'users' : users,
        'fields': fields,
        'form': form,
        'formset': formset
        })

def excel_column_map():
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
        column_map = excel_column_map()
        f = request.FILES['file']
        filename = f.name
        wb = xlrd.open_workbook(filename=None, file_contents=f.read())
        decision_items = []
        for sheet in wb.sheets():
            for row in range(app_settings['EXCEL_STARTING_ROW_COLUMN'] - 1, sheet.nrows):
                decision_item = DecisionItem()
                for key in app_settings['EXCEL_IMPORT_TEMPLATE'].keys():
                    column_name = app_settings['EXCEL_IMPORT_TEMPLATE'][key]
                    try:
                        setattr(decision_item, key, sheet.cell(row, column_map[column_name]).value)
                    except:
                        pass
                decision_items.append(decision_item)
        fields = DecisionItemLookup.get_all_fields()
        html = render_to_string('deliverables/includes/decision_items_import_table.html', {
            'decision_items': decision_items,
            'fields': fields,
            'filename': filename
            })
    return HttpResponse(html)

@login_required
def deliverable(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    return render(request, 'deliverables/summary.html', { 'deliverable' : deliverable })

@login_required
def stakeholders(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    users = User.objects.filter(is_active=True).exclude(pk=request.user.pk)
    return render(request, 'deliverables/stakeholders.html', { 'deliverable' : deliverable, 'users' : users })

@login_required
def decision_items(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    return render(request, 'deliverables/decision_items.html', { 'deliverable' : deliverable })
