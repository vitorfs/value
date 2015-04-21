from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms.models import inlineformset_factory
from value.measures.models import Measure, MeasureValue
from value.measures.forms import MeasureForm
from django.contrib import messages

@login_required
@user_passes_test(lambda user: user.is_superuser)
def measures(request):
    measures = Measure.objects.all().order_by('name')
    return render(request, 'measures/measures.html', { 'measures' : measures })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def add(request):
    MeasureValueFormSet = inlineformset_factory(Measure, MeasureValue, fields=('description',), extra=1)
    if request.method == 'POST':
        form = MeasureForm(request.POST)
        formset = MeasureValueFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            form.instance.created_by = request.user
            measure = form.save()
            formset = MeasureValueFormSet(request.POST, instance=measure)
            if formset.is_valid():
                formset.save()
                messages.success(request, u'The measure {0} was added successfully.'.format(measure.name))
                return redirect(reverse('measures:measures'))
        else:
            messages.error(request, u'Please correct the error below.')
    else:
        measure = Measure()
        form = MeasureForm(instance=measure)
        formset = MeasureValueFormSet(instance=measure)
    return render(request, 'measures/measure.html', { 'form' : form, 'formset' : formset })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def measure(request, measure_id):
    measure = get_object_or_404(Measure, pk=measure_id)
    MeasureValueFormSet = inlineformset_factory(Measure, MeasureValue, fields=('description',), extra=1)
    if request.method == 'POST':
        form = MeasureForm(request.POST, instance=measure)
        formset = MeasureValueFormSet(request.POST, instance=measure)
        if form.is_valid() and formset.is_valid():
            form.instance.updated_by = request.user
            form.save()
            formset.save()
            messages.success(request, u'The measure {0} was changed successfully.'.format(measure.name))
            return redirect(reverse('measures:measures'))
        else:
            messages.error(request, u'Please correct the error below.')
    else:
        form = MeasureForm(instance=measure)
        formset = MeasureValueFormSet(instance=measure)
    return render(request, 'measures/measure.html', { 'form' : form, 'formset' : formset })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def delete(request, measure_id):
    measure = get_object_or_404(Measure, pk=measure_id)
    if request.method == 'POST':
        measure.delete()
        messages.success(request, u'The measure {0} was deleted successfully.'.format(measure.name))
        return redirect(reverse('measures:measures'))
    return render(request, 'measures/delete.html', { 'measure' : measure })
    