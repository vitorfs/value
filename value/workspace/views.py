from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
@user_passes_test(lambda user: user.is_superuser)
def index(request):
    return render(request, 'workspace/index.html')

@login_required
@user_passes_test(lambda user: user.is_superuser)
def instance(request, model_id):
    return render(request, 'workspace/instance.html')
