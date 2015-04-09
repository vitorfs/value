from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.forms.models import modelform_factory
from django.contrib import messages

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
            return redirect(reverse('users:user', args=(user.username,)))
    else:
        user = User()
        form = UserCreationForm(instance=user)
    return render(request, 'users/add.html', { 'form' : form })

@login_required
def user(request, username):
    Form = modelform_factory(User, form=UserChangeForm, exclude=('date_joined', 'email',))
    page_user = User.objects.get(username=username)
    if request.method == 'POST':
        form = Form(request.POST, instance=page_user)
        if form.is_valid():
            form.save()
            messages.success(request, u'The user {0} was changed successfully.'.format(page_user.username))
            return redirect(reverse('users:users'))
    else:
        form = Form(instance=page_user)
    return render(request, 'users/user.html', { 'page_user' : page_user, 'form' : form })

@login_required
def password(request, username):
    page_user = User.objects.get(username=username)
    if request.method == 'POST':
        form = AdminPasswordChangeForm(page_user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, u'Password changed successfully.')
            if request.user == page_user:
                update_session_auth_hash(request, form.user)
            return redirect(reverse('users:user', args=(page_user.username,)))
    else:
        form = AdminPasswordChangeForm(page_user)
    return render(request, 'users/password.html', { 'page_user' : page_user, 'form' : form })

@login_required
def delete(request, username):
    page_user = User.objects.get(username=username)
    if request.method == 'POST':
        page_user.delete()
        messages.success(request, u'The user {0} was deleted successfully.'.format(page_user.username))
        return redirect(reverse('users:users'))
    return render(request, 'users/delete.html', { 'page_user' : page_user })
