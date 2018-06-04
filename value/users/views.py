# coding: utf-8

import json

from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.forms.models import modelform_factory
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext as _

from value.users.forms import AccountForm


@login_required
@user_passes_test(lambda user: user.is_superuser)
def users(request):
    users = User.objects.all().order_by('username')
    return render(request, 'users/index.html', {'users': users})


@login_required
@user_passes_test(lambda user: user.is_superuser)
def add(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                _(u'The user {0} was added successfully. You may edit it again below.').format(user.username)
            )
            return redirect(reverse('users:user', args=(user.pk,)))
        else:
            messages.error(request, _(u'Please correct the error below.'))
    else:
        user = User()
        form = UserCreationForm(instance=user)
    return render(request, 'users/add.html', {'form': form})


@login_required
@user_passes_test(lambda user: user.is_superuser)
def user(request, user_id):
    Form = modelform_factory(User, form=UserChangeForm, exclude=('date_joined', 'is_superuser', 'is_staff',))
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = Form(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, _(u'The user {0} was changed successfully.').format(user.username))
            return redirect(reverse('users:users'))
        else:
            messages.error(request, _(u'Please correct the error below.'))
    else:
        form = Form(instance=user)
    return render(request, 'users/edit.html', {'form': form})


@login_required
@user_passes_test(lambda user: user.is_superuser)
def password(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = AdminPasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _(u'Password changed successfully.'))
            if request.user == user:
                update_session_auth_hash(request, form.user)
            return redirect(reverse('users:user', args=(user.pk,)))
        else:
            messages.error(request, _(u'Please correct the error below.'))
    else:
        form = AdminPasswordChangeForm(user)
    return render(request, 'users/password.html', {'form': form})


@login_required
@user_passes_test(lambda user: user.is_superuser)
def delete(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    can_delete = (
        not user.meetingstakeholder_set.exists() and
        not user.evaluation_set.exists() and
        not user.deliverable_creation_user.exists() and
        not user.deliverable_manager_user.exists() and
        not user.deliverable_set.exists() and
        not user.deliverable_update_user.exists() and
        not user.meetings_created.exists() and
        not user.meetings_updated.exists() and
        not user.article_creation_user.exists() and
        not user.article_update_user.exists() and
        not user.rationales_created.exists()
    )
    if request.method == 'POST':
        user.delete()
        messages.success(request, _(u'The user {0} was deleted successfully.').format(user.username))
        return redirect(reverse('users:users'))
    return render(request, 'users/delete.html', {'delete_user': user, 'can_delete': can_delete})


@login_required
@user_passes_test(lambda user: user.is_superuser)
@require_POST
def toggle_active(request):
    user_id = request.POST.get('id')
    try:
        user = User.objects.get(pk=user_id)
        user.is_active = not user.is_active
        user.save()
        return JsonResponse({'message': _('Changes successfully saved!')})
    except User.DoesNotExist:
        return HttpResponseBadRequest()


@login_required
@user_passes_test(lambda user: user.is_superuser)
def roles(request):
    users = User.objects.all()
    roles = Group.objects.all()
    return render(request, 'users/roles.html', {'users': users, 'roles': roles})


@login_required
@user_passes_test(lambda user: user.is_superuser)
def add_role(request):
    RoleForm = modelform_factory(Group, fields=('name',))
    json_context = dict()
    if request.method == 'POST':
        form = RoleForm(request.POST, prefix='add')
        if form.is_valid():
            role = form.save()
            json_context['is_valid'] = True
            json_context['redirect_to'] = reverse('users:roles')
            messages.success(request, _(u'Role {0} successfully added!').format(role.name))
        else:
            json_context['is_valid'] = False
    else:
        form = RoleForm(prefix='add')
    context = RequestContext(request, {'form': form})
    json_context['html'] = render_to_string('includes/form_vertical.html', context)
    dump = json.dumps(json_context)
    return HttpResponse(dump, content_type='application/json')


@login_required
@user_passes_test(lambda user: user.is_superuser)
def edit_role(request, role_id):
    RoleForm = modelform_factory(Group, fields=('name',))
    role = Group.objects.get(pk=role_id)
    json_context = dict()
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role, prefix='edit')
        if form.is_valid():
            role = form.save()
            json_context['is_valid'] = True
            json_context['redirect_to'] = reverse('users:roles')
            messages.success(request, _(u'Role {0} successfully edited!').format(role.name))
        else:
            json_context['is_valid'] = False
    else:
        form = RoleForm(instance=role, prefix='edit')
    context = RequestContext(request, {'form': form})
    json_context['html'] = render_to_string('includes/form_vertical.html', context)
    dump = json.dumps(json_context)
    return HttpResponse(dump, content_type='application/json')


@login_required
@require_POST
@user_passes_test(lambda user: user.is_superuser)
def delete_role(request):
    try:
        role_id = request.POST.get('role')
        role = Group.objects.get(pk=role_id)
        role.delete()
        messages.success(request, _(u'The role {0} was deleted successfully.').format(role.name))
    except Group.DoesNotExist:
        pass
    return redirect(reverse('users:roles'))


@login_required
@user_passes_test(lambda user: user.is_superuser)
def add_user_role(request):
    user_id = request.POST.get('user')
    group_id = request.POST.get('role')
    user_role = User.objects.get(pk=user_id)
    group = Group.objects.get(pk=group_id)
    user_role.groups.add(group)
    return JsonResponse({'message': _('Changes successfully saved!')})


@login_required
@user_passes_test(lambda user: user.is_superuser)
def remove_user_role(request):
    user_id = request.POST.get('user')
    group_id = request.POST.get('role')
    user_role = User.objects.get(pk=user_id)
    group = Group.objects.get(pk=group_id)
    user_role.groups.remove(group)
    return JsonResponse({'message': _('Changes successfully saved!')})


@login_required
def account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _(u'Your profile was changed successfully.'))
        else:
            messages.error(request, _(u'Please correct the error below.'))
    else:
        form = AccountForm(instance=request.user)
    return render(request, 'users/account.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _(u'Password changed successfully.'))
            update_session_auth_hash(request, form.user)
        else:
            messages.error(request, _(u'Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})
