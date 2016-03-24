# coding: utf-8

try:
    import cPickle as pickle
except:
    import pickle

from django.db import transaction
from django.db.models.functions import Lower
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext as _

from value.deliverables.models import DecisionItemLookup
from value.application_settings.models import ApplicationSetting


@login_required
@user_passes_test(lambda user: user.is_superuser)
def index(request):
    users = User.objects.filter(is_active=True, is_superuser=False).order_by(Lower('username'))
    admins = User.objects.filter(is_active=True, is_superuser=True).order_by(Lower('username'))
    return render(request, 'application_settings/index.html', {'admins': admins, 'users': users})


@login_required
@user_passes_test(lambda user: user.is_superuser)
@require_POST
def admins(request):
    grant_ids = request.POST.getlist('grant_user')
    grant_ids = filter(None, grant_ids)
    if any(grant_ids):
        User.objects.filter(id__in=grant_ids).update(is_superuser=True)

    revoke_ids = request.POST.getlist('revoke_user')
    revoke_ids = filter(None, revoke_ids)
    if any(revoke_ids):
        User.objects.filter(id__in=revoke_ids).update(is_superuser=False)

    messages.success(request, _(u'Administrators settings saved successfully!'))
    return redirect(reverse('settings:index'))


@login_required
@user_passes_test(lambda user: user.is_superuser)
def items(request):
    custom_fields_range = range(1, 31)
    custom_fields = DecisionItemLookup.get_custom_fields()
    column_types = DecisionItemLookup.COLUMN_TYPES
    decision_items_fields = DecisionItemLookup.get_visible_fields()
    app_settings = ApplicationSetting.get()
    return render(request, 'application_settings/items.html', {
        'custom_fields_range': custom_fields_range,
        'custom_fields': custom_fields,
        'column_types': column_types,
        'decision_items_fields': decision_items_fields,
        'app_settings': app_settings
        })


@login_required
@user_passes_test(lambda user: user.is_superuser)
@require_POST
def save_ordering(request):
    try:
        setting, created = ApplicationSetting.objects.get_or_create(
            name=ApplicationSetting.DECISION_ITEMS_COLUMNS_DISPLAY
        )
        setting.value = request.POST.get('column_display')
        setting.save()
        messages.success(request, _(u'Ordering and column display saved successfully.'))
    except:
        messages.error(request, _(u'An error ocurred while trying to save your data.'))
    return redirect(reverse('settings:items'))


@login_required
@user_passes_test(lambda user: user.is_superuser)
@transaction.atomic
@require_POST
def save_custom_fields(request):
    DecisionItemLookup.objects.all().delete()
    custom_columns = range(1, 31)
    column_display = u'name,description,'
    for column in custom_columns:
        is_active = request.POST.get('column_is_active_{0}'.format(column))
        if is_active:
            item = DecisionItemLookup()
            item.column_name = 'column_{0}'.format(column)
            label = request.POST.get('column_label_{0}'.format(column))[:255]
            if not label:
                label = item.column_name
            item.column_label = label
            item.column_type = request.POST.get('column_type_{0}'.format(column), 'S')
            display = request.POST.get('column_display_{0}'.format(column))
            if display:
                item.column_display = True
                column_display += '{0},'.format(item.column_name)
            else:
                item.column_display = False
            item.save()
    setting, created = ApplicationSetting.objects.get_or_create(name=ApplicationSetting.DECISION_ITEMS_COLUMNS_DISPLAY)
    setting.value = column_display
    setting.save()

    messages.success(request, _(u'Custom fields were saved successfully.'))
    return redirect(reverse('settings:items'))


@login_required
@user_passes_test(lambda user: user.is_superuser)
def import_template(request):
    import_template_fields = DecisionItemLookup.get_all_fields()
    app_settings = ApplicationSetting.get()
    return render(request, 'application_settings/import.html', {
        'import_template_fields': import_template_fields,
        'app_settings': app_settings
        })


@login_required
@user_passes_test(lambda user: user.is_superuser)
@transaction.atomic
@require_POST
def save_import_templates(request):
    orientation, created = ApplicationSetting.objects.get_or_create(name=ApplicationSetting.EXCEL_ENTRY_ORIENTATION)
    orientation.value = request.POST.get('orientation')
    orientation.save()

    starting_row_column, created = ApplicationSetting.objects.get_or_create(
        name=ApplicationSetting.EXCEL_STARTING_ROW_COLUMN
    )
    starting_row_column.value = request.POST.get('starting_row_column')
    starting_row_column.save()

    decision_items_fields = DecisionItemLookup.get_all_fields()
    template = {}
    input_name = 'column'
    if orientation.value == 'column':
        input_name = 'row'
    for name, field in decision_items_fields.items():
        if request.POST.get('active_{0}'.format(name)):
            template[name] = request.POST.get('{0}_{1}'.format(input_name, name))
    import_template, created = ApplicationSetting.objects.get_or_create(name=ApplicationSetting.EXCEL_IMPORT_TEMPLATE)
    import_template.value = pickle.dumps(template)
    import_template.save()

    excel_sheet_index, created = ApplicationSetting.objects.get_or_create(name=ApplicationSetting.EXCEL_SHEET_INDEX)
    excel_sheet_index.value = request.POST.get('excel_sheet_index')
    excel_sheet_index.save()

    messages.success(request, _(u'Import templates saved successfully.'))
    return redirect(reverse('settings:import'))
