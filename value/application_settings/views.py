from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

@login_required
@user_passes_test(lambda user: user.is_superuser)
def index(request):
    admins = User.objects.filter(is_superuser=True)
    return render(request, 'application_settings/index.html', { 'admins': admins })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def items(request):
    custom_columns = range(1, 31)
    return render(request, 'application_settings/items.html', { 'custom_columns': custom_columns })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def notifications(request):
    return render(request, 'application_settings/notifications.html')