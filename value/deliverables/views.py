from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from value.deliverables.models import Deliverable, DecisionItem


@login_required
def index(request):
    deliverables = Deliverable.objects.all().order_by('-updated_at')
    return render(request, 'deliverables/index.html', { 'deliverables' : deliverables })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def new(request):
    if request.method == 'POST':
        deliverable = Deliverable()
        deliverable.name = request.POST.get('name')
        deliverable.description = request.POST.get('description')
        deliverable.manager = request.user
        deliverable.created_by = request.user
        deliverable.save()

        users_id = request.POST.getlist('stakeholders')
        deliverable.stakeholders = User.objects.filter(pk__in=users_id)
        deliverable.stakeholders.add(request.user)
        deliverable.save()

        items_names = request.POST.getlist('decision_item')
        for name in items_names:
            item = DecisionItem()
            item.deliverable = deliverable
            item.name = name
            item.created_by = request.user
            item.save()

        messages.success(request, u'The deliverable {0} was added successfully.'.format(deliverable.name))
        return redirect(reverse('deliverables:index'))
    users = User.objects.filter(is_active=True).exclude(pk=request.user.pk)
    return render(request, 'deliverables/new.html', { 'users' : users })

@login_required
def deliverable(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    return render(request, 'deliverables/summary.html', { 'deliverable' : deliverable })

@login_required
def stakeholders(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    users = User.objects.filter(is_active=True).exclude(pk=request.user.pk)
    return render(request, 'deliverables/stakeholders.html', { 'deliverable' : deliverable, 'users' : users })

@login_required
def decision_items(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    return render(request, 'deliverables/decision_items.html', { 'deliverable' : deliverable })
