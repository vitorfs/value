# coding: utf-8

import json

from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.forms.models import modelform_factory
from django.template import RequestContext
from django.template.loader import render_to_string

from value.factors.models import Factor
from value.users.forms import AccountForm


@login_required
@user_passes_test(lambda user: user.is_superuser)
def users(request):
    users = User.objects.all().order_by('username')
    return render(request, 'users/index.html', { 'users' : users })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def add(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, u'The user {0} was added successfully. You may edit it again below.'.format(user.username))
            return redirect(reverse('users:user', args=(user.pk,)))
        else:
            messages.error(request, u'Please correct the error below.')
    else:
        user = User()
        form = UserCreationForm(instance=user)
    return render(request, 'users/add.html', { 'form' : form })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def user(request, user_id):
    Form = modelform_factory(User, form=UserChangeForm, exclude=('date_joined', 'is_superuser', 'is_staff',))
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = Form(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, u'The user {0} was changed successfully.'.format(user.username))
            return redirect(reverse('users:users'))
        else:
            messages.error(request, u'Please correct the error below.')
    else:
        form = Form(instance=user)
    return render(request, 'users/edit.html', { 'form' : form })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def password(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = AdminPasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, u'Password changed successfully.')
            if request.user == user:
                update_session_auth_hash(request, form.user)
            return redirect(reverse('users:user', args=(user.pk,)))
        else:
            messages.error(request, u'Please correct the error below.')
    else:
        form = AdminPasswordChangeForm(user)
    return render(request, 'users/password.html', { 'form' : form })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def delete(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, u'The user {0} was deleted successfully.'.format(user.username))
        return redirect(reverse('users:users'))
    return render(request, 'users/delete.html', { 'delete_user' : user })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def roles(request):
    return render(request, 'users/roles.html')

def add_role(request):
    RoleForm = modelform_factory(Group, fields=('name',))
    json_context = dict()
    if request.method == 'POST':
        form = RoleForm(request.POST, prefix='add')
        if form.is_valid():
            role = form.save()
            json_context['is_valid'] = True
            messages.success(request, u'Role {0} successfully added!'.format(role.name))
        else:
            json_context['is_valid'] = False
    else:
        form = RoleForm(prefix='add')
    context = RequestContext(request, { 'form': form })
    json_context['html'] = render_to_string('includes/form_vertical.html', context)
    dump = json.dumps(json_context)
    return HttpResponse(dump, content_type='application/json')

@login_required
def account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, u'Your profile was changed successfully.')
        else:
            messages.error(request, u'Please correct the error below.')
    else:
        form = AccountForm(instance=request.user)
    return render(request, 'users/account.html', { 'form' : form })

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, u'Password changed successfully.')
            update_session_auth_hash(request, form.user)
        else:
            messages.error(request, u'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', { 'form' : form })
