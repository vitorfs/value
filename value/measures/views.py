# coding: utf-8

from django.db import transaction
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms.models import inlineformset_factory
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext as _

from value.measures.models import Measure, MeasureValue
from value.measures.forms import CreateMeasureForm, ChangeMeasureForm


@login_required
@user_passes_test(lambda user: user.is_superuser)
def index(request):
    measures = Measure.objects.all().order_by('name')
    return render(request, 'measures/index.html', {'measures': measures})


@login_required
@user_passes_test(lambda user: user.is_superuser)
@transaction.atomic
def add(request):
    MeasureValueFormSet = inlineformset_factory(
        Measure,
        MeasureValue,
        fields=('description', 'order', 'color'),
        extra=0,
        min_num=2,
        validate_min=True
    )
    if request.method == 'POST':
        form = CreateMeasureForm(request.POST)
        formset = MeasureValueFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            measure = form.save()
            formset.instance = measure
            formset.save()
            messages.success(request, _(u'The measure {0} was added successfully.').format(measure.name))
            return redirect(reverse('measures:index'))
        else:
            messages.error(request, _(u'Please correct the error below.'))
    else:
        measure = Measure()
        form = CreateMeasureForm()
        formset = MeasureValueFormSet()
    return render(request, 'measures/add.html', {'form': form, 'formset': formset})


@login_required
@user_passes_test(lambda user: user.is_superuser)
@transaction.atomic
def edit(request, measure_id):
    measure = get_object_or_404(Measure, pk=measure_id)
    MeasureValueFormSet = inlineformset_factory(
        Measure,
        MeasureValue,
        fields=('description', 'order', 'color'),
        extra=0
    )
    can_edit = (not measure.deliverables.exists() and not measure.meetings.exists())
    if request.method == 'POST':
        form = ChangeMeasureForm(request.POST, instance=measure)
        formset = MeasureValueFormSet(request.POST, instance=measure)
        if form.is_valid() and formset.is_valid():
            form.save()
            if can_edit:
                formset.save()
                for value in measure.measurevalue_set.all():
                    if not value.description.strip():
                        value.delete()
            messages.success(request, _(u'The measure {0} was changed successfully.').format(measure.name))
            return redirect(reverse('measures:index'))
        else:
            messages.error(request, _(u'Please correct the error below.'))
    else:
        form = ChangeMeasureForm(instance=measure)
        formset = MeasureValueFormSet(instance=measure)
    return render(request, 'measures/edit.html', {'form': form, 'formset': formset, 'can_edit': can_edit})


@login_required
@user_passes_test(lambda user: user.is_superuser)
def delete(request, measure_id):
    measure = get_object_or_404(Measure, pk=measure_id)
    can_delete = (not measure.deliverables.exists() and not measure.meetings.exists())
    if request.method == 'POST' and can_delete:
        measure.delete()
        messages.success(request, _(u'The measure {0} was deleted successfully.').format(measure.name))
        return redirect(reverse('measures:index'))
    return render(request, 'measures/delete.html', {'measure': measure, 'can_delete': can_delete})


@login_required
@user_passes_test(lambda user: user.is_superuser)
@require_POST
def toggle_active(request):
    measure_id = request.POST.get('id')
    try:
        measure = Measure.objects.get(pk=measure_id)
        measure.is_active = not measure.is_active
        measure.save()
        return HttpResponse()
    except Measure.DoesNotExist:
        return HttpResponseBadRequest()
