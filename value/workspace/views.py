from datetime import datetime
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from value.workspace.models import Instance, InstanceItem, InstanceItemEvaluation
from value.factors.models import Factor
from value.measures.models import Measure, MeasureValue

@login_required
def index(request):
    instances = Instance.objects.all()
    finished_instances = instances.filter(status=Instance.FINISHED).order_by('-updated_at')
    wip_instances = instances.exclude(status=Instance.FINISHED).order_by('-updated_at')
    return render(request, 'workspace/index.html', { 'finished_instances' : finished_instances, 'wip_instances' : wip_instances })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def new(request):
    if request.method == 'POST':
        instance = Instance()
        instance.name = request.POST.get('name')
        instance.description = request.POST.get('description')
        instance.manager = request.user
        instance.created_by = request.user
        instance.save()

        users_id = request.POST.getlist('stakeholders')
        instance.stakeholders = User.objects.filter(pk__in=users_id)
        instance.save()

        items_names = request.POST.getlist('instance_item')
        for name in items_names:
            item = InstanceItem()
            item.instance = instance
            item.name = name
            item.save()

        messages.success(request, u'The value project {0} was added successfully.'.format(instance.name))
        return redirect(reverse('workspace:index'))
    users = User.objects.filter(is_active=True).exclude(pk=request.user.pk)
    return render(request, 'workspace/wizard.html', { 'users' : users })

@login_required
def instance(request, instance_id):
    instance = get_object_or_404(Instance, pk=instance_id)
    return render(request, 'workspace/summary.html', { 'instance' : instance })

@login_required
def evaluate(request, instance_id):
    instance = get_object_or_404(Instance, pk=instance_id)
    factors = Factor.get_factors()
    evaluations = InstanceItemEvaluation.get_user_evaluations_by_instance(user=request.user, instance=instance)
    items = instance.get_items()
    total_items = items.count()
    search_query = request.GET.get('search')
    if search_query:
        items = items.filter(name__icontains=search_query)
    return render(request, 'workspace/evaluate.html', { 
        'instance' : instance, 
        'factors' : factors, 
        'evaluations' : evaluations,
        'total_items': total_items,
        'items': items,
        'search_query': search_query
        })

@login_required
def save_evaluation(request, instance_id):
    instance = get_object_or_404(Instance, pk=instance_id)

    item_id = request.POST.get('item_id')
    item = get_object_or_404(InstanceItem, pk=item_id)

    factor_id = request.POST.get('factor_id')
    factor = get_object_or_404(Factor, pk=factor_id)

    measure_id = request.POST.get('measure_id')
    measure = get_object_or_404(Measure, pk=measure_id)

    measure_value_id = request.POST.get('measure_value_id')
    measure_value = get_object_or_404(MeasureValue, pk=measure_value_id)

    evaluation, created = InstanceItemEvaluation.objects.get_or_create(instance=instance, item=item, user=request.user, factor=factor, measure=measure)

    if evaluation.measure_value == measure_value and not created:
        evaluation.delete()
    else:
        evaluation.evaluated_at = datetime.now()
        evaluation.measure_value = measure_value
        evaluation.save()

    return HttpResponse('')

@login_required
def stakeholders(request, instance_id):
    instance = get_object_or_404(Instance, pk=instance_id)
    users = User.objects.filter(is_active=True).exclude(pk=request.user.pk)
    return render(request, 'workspace/stakeholders.html', { 'instance' : instance, 'users' : users })

@login_required
def backlog(request, instance_id):
    instance = get_object_or_404(Instance, pk=instance_id)
    backlog = instance.get_items()
    return render(request, 'workspace/backlog.html', { 'instance' : instance, 'backlog' : backlog })

@login_required
def meetings(request, instance_id):
    pass

@login_required
def new_meeting(request, instance_id):
    instance = get_object_or_404(Instance, pk=instance_id)
    return render(request, 'workspace/new_meeting.html', { 'instance' : instance })

@login_required
def meeting(request, instance_id, meeting_id):
    pass
