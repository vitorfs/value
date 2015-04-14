from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
def index(request):
    return render(request, 'help/index.html')
    