from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
def index(request):
    return render(request, 'workspace/index.html')

@login_required
@user_passes_test(lambda user: user.is_superuser)
def new(request):
    return render(request, 'workspace/new.html')

@login_required
def instance(request, instance_id):
    return render(request, 'workspace/instance.html')
