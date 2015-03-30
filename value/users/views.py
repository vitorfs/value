from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

@login_required
def users(request):
    users = User.objects.all()
    return render(request, 'users/users.html', { 'users' : users })

@login_required
def user(request, username):
    page_user = User.objects.get(username=username)
    form = UserChangeForm(instance=page_user)
    return render(request, 'users/user.html', { 'page_user' : page_user, 'form' : form })

@login_required
def password(request, username):
    return render(request, 'users/users.html')