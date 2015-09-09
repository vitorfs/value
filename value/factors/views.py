# coding: utf-8

from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseBadRequest

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
    factor_has_relations = factor.deliverables.exists()
    associated_deliverables = factor.deliverables.values_list('name', flat=True)
    str_associated_deliverables = ', '.join(associated_deliverables)
    messages.warning(request, u'The factor {0} is associated with deliverables. Deleting this factor will lead to data loss. If you really want to delete this factor from the system, please delete the associated deliverables first: {1}.'.format(factor.name, str_associated_deliverables))
    if request.method == 'POST' and not factor_has_relations:
        factor.delete()
        messages.success(request, u'The factor {0} was deleted successfully.'.format(factor.name))
        return redirect(reverse('factors:factors'))
    return render(request, 'factors/delete.html', { 'factor': factor })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def groups(request):
    groups = Group.objects.all()
    available_factors = Factor.list().filter(group=None)
    form = GroupForm()
    return render(request, 'factors/groups.html', { 
            'groups': groups,
            'available_factors': available_factors,
            'form': form 
        })

@login_required
@require_POST
@user_passes_test(lambda user: user.is_superuser)
def add_group(request):
    form = GroupForm(request.POST)
    if form.is_valid():
        group = form.save()
        messages.success(request, u'Group {0} successfully added!'.format(group.name))
    else:
        messages.error(request, u'Name is a required field!')
    return redirect(reverse('factors:groups'))

@login_required
@user_passes_test(lambda user: user.is_superuser)
def edit_group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            group = form.save()
            messages.success(request, u'Group {0} successfully edited!'.format(group.name))
        else:
            messages.error(request, u'Name is a required field!')
        return redirect(reverse('factors:groups'))
    else:
        form = GroupForm(instance=group)
        return render(request, 'factors/edit_group_form.html', { 'form': form })

@login_required
@require_POST
@user_passes_test(lambda user: user.is_superuser)
def delete_group(request):
    try:
        group_id = request.POST.get('group')
        group = Group.objects.get(pk=group_id)
        group.delete()
        messages.success(request, u'The group {0} was deleted successfully.'.format(group.name))
    except Group.DoesNotExist:
        pass
    return redirect(reverse('factors:groups'))

@login_required
@require_POST
@user_passes_test(lambda user: user.is_superuser)
def add_factor_group(request):
    factor_id = request.POST.get('factor')
    group_id = request.POST.get('group', None)

    factor = Factor.objects.get(pk=factor_id)
    group = None
    if group_id:
        group = Group.objects.get(pk=group_id)
    factor.group = group
    factor.save()
    return HttpResponse()
