from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from value.factors.models import Factor
from value.factors.forms import FactorForm

@login_required
@user_passes_test(lambda user: user.is_superuser)
def factors(request):
    factors = Factor.objects.all().order_by('name')
    return render(request, 'factors/factors.html', { 'factors' : factors })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def add(request):
    if request.method == 'POST':
        form = FactorForm(request.POST)
        if form.is_valid():
            form.instance.created_by = request.user
            factor = form.save()
            messages.success(request, u'The factor {0} was added successfully.'.format(factor.name))
            return redirect(reverse('factors:factors'))
        else:
            messages.error(request, u'Please correct the error below.')
    else:
        factor = Factor()
        form = FactorForm(instance=factor)
    return render(request, 'factors/factor.html', { 'form' : form })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def factor(request, factor_id):
    factor = get_object_or_404(Factor, pk=factor_id)
    if request.method == 'POST':
        form = FactorForm(request.POST, instance=factor)
        if form.is_valid():
            form.instance.updated_by = request.user
            factor = form.save()
            messages.success(request, u'The factor {0} was changed successfully.'.format(factor.name))
            return redirect(reverse('factors:factors'))
        else:
            messages.error(request, u'Please correct the error below.')
    else:
        form = FactorForm(instance=factor)
    return render(request, 'factors/factor.html', { 'form' : form })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def delete(request, factor_id):
    factor = get_object_or_404(Factor, pk=factor_id)
    if request.method == 'POST':
        factor.delete()
        messages.success(request, u'The factor {0} was deleted successfully.'.format(factor.name))
        return redirect(reverse('factors:factors'))
    return render(request, 'factors/delete.html', { 'factor' : factor })
