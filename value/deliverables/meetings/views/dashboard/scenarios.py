# coding: utf-8

import json

from django import forms
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.loader import render_to_string

from value.deliverables.meetings.models import Meeting, Scenario
from value.deliverables.meetings.forms import ScenarioForm, FactorsScenarioBuilderForm, FactorsGroupsScenarioBuilderForm


@login_required
def add_scenario(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    scenario = Scenario(meeting=meeting)
    json_context = dict()
    if request.method == 'POST':
        form = ScenarioForm(request.POST, instance=scenario, prefix='add')
        is_valid = json_context['is_valid'] = form.is_valid()
        if is_valid:
            form.save()
    else:
        form = ScenarioForm(instance=scenario, prefix='add')
    context = RequestContext(request, { 'form': form })
    json_context['form'] = render_to_string('meetings/dashboard/includes/partial_scenario_form.html', context)
    return HttpResponse(json.dumps(json_context), content_type='application/json')

@login_required
def edit_scenario(request, deliverable_id, meeting_id, scenario_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    json_context = dict()
    if request.method == 'POST':
        form = ScenarioForm(request.POST, instance=scenario, prefix='edit')
        is_valid = json_context['is_valid'] = form.is_valid()
        if is_valid:
            form.save()
    else:
        form = ScenarioForm(instance=scenario, prefix='edit')
    context = RequestContext(request, { 'form': form })
    json_context['form'] = render_to_string('meetings/dashboard/includes/partial_scenario_form.html', context)
    return HttpResponse(json.dumps(json_context), content_type='application/json')

@login_required
def details_scenario(request, deliverable_id, meeting_id, scenario_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    return render(request, 'meetings/dashboard/includes/scenario_details.html', {
        'meeting': meeting,
        'scenario': scenario
        })

@require_POST
@login_required
def delete_scenario(request, deliverable_id, meeting_id):
    scenario_id = request.POST.get('scenario')
    next = request.POST.get('next', reverse('deliverables:meetings:dashboard', args=(deliverable_id, meeting_id)))
    try:
        scenario = Scenario.objects.get(pk=scenario_id)
        scenario.delete()
        messages.success(request, u'Scenario {0} successfully deleted!'.format(scenario.name))
    except Scenario.DoesNotExist:
        messages.error(request, 'An unexpected error ocurred.')
    return redirect(next)

def get_scenario_builder_form(category):
    ScenarioBuilderForm = forms.Form
    if category in (Scenario.FACTORS, Scenario.ACCEPTANCE):
        ScenarioBuilderForm = FactorsScenarioBuilderForm
    elif category == Scenario.FACTORS_GROUPS:
        ScenarioBuilderForm = FactorsGroupsScenarioBuilderForm
    return ScenarioBuilderForm

@login_required
def scenario_builder(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    json_context = dict()
    category = request.GET.get('category', request.POST.get('category'))
    ScenarioBuilderForm = get_scenario_builder_form(category)

    if request.method == 'POST':
        form = ScenarioBuilderForm(request.POST, initial={ 'meeting': meeting })
        if form.is_valid():
            scenario = Scenario(meeting=meeting, category=category)
            scenario.build(**form.cleaned_data)
            json_context['is_valid'] = True
        else:
            json_context['is_valid'] = False
    else:
        form = ScenarioBuilderForm(initial={ 'meeting': meeting, 'category': category })

    context = RequestContext(request, { 'form': form })
    json_context['form'] = render_to_string('includes/form_vertical.html', context)
    return HttpResponse(json.dumps(json_context), content_type='application/json')
