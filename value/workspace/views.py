from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

@login_required
def index(request):
    return render(request, 'workspace/index.html')

@login_required
@user_passes_test(lambda user: user.is_superuser)
def new(request):
    users = User.objects.all()
    return render(request, 'workspace/new.html', { 'users' : users })

@login_required
def instance(request, instance_id):
    return render(request, 'workspace/instance.html')
