from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from value.factors.models import Factor
from value.factors.forms import FactorForm

@login_required
def factors(request):
    factors = Factor.objects.all()
    return render(request, 'factors/factors.html', { 'factors' : factors })

@login_required
def add(request):
    if request.method == 'POST':
        form = FactorForm(request.POST)
        if form.is_valid():
            form.instance.created_by = request.user
            factor = form.save()
            messages.success(request, u'The factor {0} was added successfully.'.format(factor.name))
            return redirect(reverse('factors:factors'))
    else:
        factor = Factor()
        form = FactorForm(instance=factor)
    return render(request, 'factors/factor.html', { 'form' : form })
