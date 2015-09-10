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
    measure_has_relations = measure.deliverables.exists()
    if measure_has_relations:
        associated_deliverables = measure.deliverables.values_list('name', flat=True)
        str_associated_deliverables = ', '.join(associated_deliverables)
        messages.warning(request, u'The measure {0} is associated with deliverables. Deleting this measure will lead to data loss. If you really want to delete this measure from the system, please delete the associated deliverables first: {1}.'.format(measure.name, str_associated_deliverables))
    if request.method == 'POST' and not measure_has_relations:
        measure.delete()
        messages.success(request, u'The measure {0} was deleted successfully.'.format(measure.name))
        return redirect(reverse('measures:index'))
    return render(request, 'measures/delete.html', { 'measure' : measure, 'can_delete': measure_has_relations })
    