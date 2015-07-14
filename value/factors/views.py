from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from value.factors.models import Factor, Group
from value.factors.forms import FactorForm, GroupForm

@login_required
@user_passes_test(lambda user: user.is_superuser)
def factors(request):
    factors = Factor.objects.all().order_by('name')
    return render(request, 'factors/factors.html', { 'factors': factors })

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
    return render(request, 'factors/factor.html', { 'form': form })

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
    return render(request, 'factors/factor.html', { 'form': form })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def delete(request, factor_id):
    factor = get_object_or_404(Factor, pk=factor_id)
    if request.method == 'POST':
        factor.delete()
        messages.success(request, u'The factor {0} was deleted successfully.'.format(factor.name))
        return redirect(reverse('factors:factors'))
    return render(request, 'factors/delete.html', { 'factor': factor })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def groups(request):
    groups = Group.objects.all()
    factors = Factor.list()
    form = GroupForm()
    return render(request, 'factors/groups.html', { 
            'groups': groups,
            'factors': factors,
            'form': form 
        })

@login_required
@user_passes_test(lambda user: user.is_superuser)
@require_POST
def add_group(request):
    form = GroupForm(request.POST)
    if form.is_valid():
        group = form.save()
        messages.success(request, u'Group {0} successfully added!'.format(group.name))
    else:
        messages.error(request, u'Name is a required field!')
    return redirect(reverse('factors:groups'))
