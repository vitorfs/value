from django.shortcuts import render
from value.factors.models import Factor
from value.factors.forms import FactorForm

def factors(request):
    return render(request, 'factors/factors.html')

def add(request):
    factor = Factor()
    form = FactorForm(instance=factor)
    return render(request, 'factors/add.html', { 'form' : form })