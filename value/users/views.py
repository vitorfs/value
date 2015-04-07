from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms.models import modelform_factory

@login_required
def users(request):
    users = User.objects.all()
    return render(request, 'users/users.html', { 'users' : users })

@login_required
def add_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(reverse('user', args=(user.username,)))
    else:
        user = User()
        form = UserCreationForm(instance=user)
    return render(request, 'users/add_user.html', { 'form' : form })

@login_required
def user(request, username):
    Form = modelform_factory(User, form=UserChangeForm, exclude=('date_joined', 'email',))
    page_user = User.objects.get(username=username)
    if request.method == 'POST':
        form = Form(request.POST, instance=page_user)
        if form.is_valid():
            form.save()
            return redirect(reverse('users'))
        else:
            print form.errors
    else:
        form = Form(instance=page_user)
    return render(request, 'users/user.html', { 'page_user' : page_user, 'form' : form })

@login_required
def password(request, username):
    return render(request, 'users/users.html')