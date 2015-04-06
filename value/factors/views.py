from django.shortcuts import render

def factors(request):
    return render(request, 'factors/factors.html')