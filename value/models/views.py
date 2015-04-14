from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
@user_passes_test(lambda user: user.is_superuser)
def models(request):
    return render(request, 'models/models.html')

@login_required
@user_passes_test(lambda user: user.is_superuser)
def model(request, model_id):
    return render(request, 'models/model.html')
