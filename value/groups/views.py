from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User

from value.groups.forms import GroupForm

@login_required
@user_passes_test(lambda user: user.is_superuser)
def index(request):
    groups = Group.objects.all().order_by('name')
    return render(request, 'groups/index.html', { 'groups': groups })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def add(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, u'The group {0} was added successfully.'.format(group.name))
            return redirect(reverse('groups:index'))
        else:
            messages.error(request, u'Please correct the error below.')
    else:
        form = GroupForm()
    return render(request, 'groups/add.html', { 'form': form })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def edit(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            group = form.save()
            messages.success(request, u'The group {0} was changed successfully.'.format(group.name))
            return redirect(reverse('groups:index'))
        else:
            messages.error(request, u'Please correct the error below.')
    else:
        form = GroupForm(instance=group, initial={ 'stakeholders': group.user_set.all() })
    return render(request, 'groups/edit.html', { 'form': form })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def delete(request, group_id):
    return render(request, 'groups/index.html')