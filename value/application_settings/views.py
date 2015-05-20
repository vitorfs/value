from django.db import transaction
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST

from value.deliverables.models import DecisionItemLookup

@login_required
@user_passes_test(lambda user: user.is_superuser)
def index(request):
    admins = User.objects.filter(is_superuser=True)
    return render(request, 'application_settings/index.html', { 'admins': admins })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def items(request):
    custom_fields_range = range(1, 31)
    custom_fields = DecisionItemLookup.get_custom_fields()
    column_types = DecisionItemLookup.COLUMN_TYPES
    return render(request, 'application_settings/items.html', { 
        'custom_fields_range': custom_fields_range,
        'custom_fields': custom_fields,
        'column_types': column_types
        })

@login_required
@user_passes_test(lambda user: user.is_superuser)
@transaction.atomic
@require_POST
def save_custom_fields(request):
    DecisionItemLookup.objects.all().delete()
    custom_columns = range(1, 31)
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
            item.save()
    messages.success(request, 'Custom fields were saved successfully.')
    return redirect(reverse('settings:items'))

@login_required
@user_passes_test(lambda user: user.is_superuser)
def notifications(request):
    return render(request, 'application_settings/notifications.html')