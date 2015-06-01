from django.db import transaction
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms.models import inlineformset_factory
from django.contrib import messages

from value.measures.models import Measure, MeasureValue
from value.measures.forms import MeasureForm


@login_required
@user_passes_test(lambda user: user.is_superuser)
def index(request):
    measures = Measure.objects.all().order_by('name')
    return render(request, 'measures/index.html', { 'measures' : measures })

@login_required
@user_passes_test(lambda user: user.is_superuser)
@transaction.atomic
def add(request):
    MeasureValueFormSet = inlineformset_factory(Measure, MeasureValue, fields=('description', 'order', 'color'), extra=1)
    if request.method == 'POST':
        form = MeasureForm(request.POST)
        formset = MeasureValueFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            form.instance.created_by = request.user
            measure = form.save()
            formset.instance = measure
            formset.save()
            for value in measure.measurevalue_set.all():
                if not value.description.strip():
                    value.delete()
            messages.success(request, u'The measure {0} was added successfully.'.format(measure.name))
            return redirect(reverse('measures:index'))
        else:
            messages.error(request, u'Please correct the error below.')
    else:
        measure = Measure()
        form = MeasureForm(instance=measure)
        formset = MeasureValueFormSet(instance=measure)
    return render(request, 'measures/add.html', { 'form' : form, 'formset' : formset })

@login_required
@user_passes_test(lambda user: user.is_superuser)
@transaction.atomic
def edit(request, measure_id):
    measure = get_object_or_404(Measure, pk=measure_id)
    MeasureValueFormSet = inlineformset_factory(Measure, MeasureValue, fields=('description', 'order', 'color'), extra=1)
    if request.method == 'POST':
        form = MeasureForm(request.POST, instance=measure)
        formset = MeasureValueFormSet(request.POST, instance=measure)
        if form.is_valid() and formset.is_valid():
            form.instance.updated_by = request.user
            form.save()
            formset.save()
            for value in measure.measurevalue_set.all():
                if not value.description.strip():
                    value.delete()
            messages.success(request, u'The measure {0} was changed successfully.'.format(measure.name))
            return redirect(reverse('measures:index'))
        else:
            messages.error(request, u'Please correct the error below.')
    else:
        form = MeasureForm(instance=measure)
        formset = MeasureValueFormSet(instance=measure)
    return render(request, 'measures/edit.html', { 'form' : form, 'formset' : formset })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def delete(request, measure_id):
    measure = get_object_or_404(Measure, pk=measure_id)
    if request.method == 'POST':
        measure.delete()
        messages.success(request, u'The measure {0} was deleted successfully.'.format(measure.name))
        return redirect(reverse('measures:index'))
    return render(request, 'measures/delete.html', { 'measure' : measure })
    