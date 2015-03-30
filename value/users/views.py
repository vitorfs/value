from django.shortcuts import render
from django.contrib.auth.models import User

def users(request):
    users = User.objects.all()
    return render(request, 'users/users.html', { 'users' : users })