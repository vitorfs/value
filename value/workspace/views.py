import json
import operator
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
    return render(request, 'workspace/dashboard.html', { 'instance' : instance })

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

    measure_value = None
    if measure_value_id:
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
def analyze(request, instance_id):
    instance = get_object_or_404(Instance, pk=instance_id)
    evaluations = InstanceItemEvaluation.get_evaluations_by_instance(instance)
    factors = Factor.get_factors()
    data = []
    for factor in factors:
        data.append([factor.name, evaluations.filter(factor=factor).exclude(measure_value=None).count()])
    dump = json.dumps(data)
    return render(request, 'workspace/analyze.html', { 'instance' : instance, 'data' : dump })

@login_required
def analyze_features(request, instance_id):

    chart_type = request.GET.get('chart', 'bar')

    instance = get_object_or_404(Instance, pk=instance_id)
    items = instance.get_items()
    evaluations = InstanceItemEvaluation.get_evaluations_by_instance(instance)

    data = {}

    measure = None

    for item in items:
        data[item.name] = {}
        item_evaluation = InstanceItemEvaluation.get_evaluations_by_instance(instance).filter(item=item)

        for e in item_evaluation:
            measure = e.measure
            data[item.name][e.factor.name] = {}
            for value in e.factor.measure.get_values():
                data[item.name][e.factor.name][value.description] = 0
            data[item.name][e.factor.name][u'None'] = 0

        for e in item_evaluation:
            mv = u'None'
            if e.measure_value:
                mv = e.measure_value.description
            data[item.name][e.factor.name][mv] = data[item.name][e.factor.name][mv] + 1

    feature_charts = {}

    for item in items:

        feature_data = data[item.name]
        sorted_data = sorted(feature_data.items(), key=operator.itemgetter(0))

        categories = []
        for factor in sorted_data:
            categories.append(factor[0])

        series = []
        for value in measure.get_values():
            serie_data = []
            for factor in sorted_data:
                serie_data.append(factor[1][value.description])
            series.append({ 'name': value.description, 'data': serie_data, 'color': value.color })

        serie_data = []
        for factor in sorted_data:
            serie_data.append(factor[1][u'None'])
        series.append({ 'name': 'N/A', 'data': serie_data, 'color': '#E7E7E7' })

        highchart_data = {
            'chart': { 'type': chart_type },
            'title': { 'text': item.name },
            'xAxis': { 'categories': categories },
            'yAxis': { 'min': 0, 'title': { 'text': 'Number of votes' } },
            'legend': { 'reversed': True },
            'plotOptions': { 'series': { 'stacking': 'normal' }},
            'series': series
        }

        dump = json.dumps(highchart_data)

        feature_charts[item.id] = dump

    return render(request, 'workspace/analyze_features.html', { 'instance' : instance, 'feature_charts' : feature_charts })
