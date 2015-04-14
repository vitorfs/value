from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.forms.models import modelform_factory
from django.contrib import messages
from value.factors.models import Factor

@login_required
def users(request):
    users = User.objects.all().order_by('username')
    return render(request, 'users/users.html', { 'users' : users })

@login_required
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
def user(request, user_id):
    Form = modelform_factory(User, form=UserChangeForm, exclude=('date_joined',))
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = Form(request.POST, instance=user)
        if form.is_valid():
            factor_ids = request.POST.getlist('id_factor')
            form.instance.profile.factors = Factor.objects.filter(is_active=True, pk__in=factor_ids)
            form.save()
            messages.success(request, u'The user {0} was changed successfully.'.format(user.username))
            return redirect(reverse('users:users'))
        else:
            messages.error(request, u'Please correct the error below.')
    else:
        form = Form(instance=user)
    factors = Factor.objects.filter(is_active=True)
    return render(request, 'users/user.html', { 'form' : form, 'factors' : factors })

@login_required
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
def delete(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, u'The user {0} was deleted successfully.'.format(user.username))
        return redirect(reverse('users:users'))
    return render(request, 'users/delete.html', { 'delete_user' : user })
