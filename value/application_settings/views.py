from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def index(request):
    admins = User.objects.filter(is_superuser=True)
    return render(request, 'application_settings/index.html', { 'admins': admins })