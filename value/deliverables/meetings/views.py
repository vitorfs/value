import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q

from value.factors.models import Factor
from value.measures.models import Measure, MeasureValue
from value.deliverables.models import Deliverable, DecisionItemLookup, Rationale
from value.deliverables.forms import RationaleForm
from value.deliverables.meetings.models import Meeting, MeetingItem, MeetingStakeholder, Evaluation
from value.deliverables.meetings.charts import Highcharts
from value.deliverables.meetings.forms import MeetingForm


@login_required
def new(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    decision_items_fields = DecisionItemLookup.get_all_fields()
    decision_items = deliverable.decisionitem_set.all()
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        stakeholder_ids = request.POST.getlist('stakeholders')
        selected_stakeholders = User.objects.filter(id__in=stakeholder_ids)
        meeting_stakeholders = User.objects.filter(Q(id__in=selected_stakeholders) | Q(id__in=deliverable.stakeholders.all())).filter(is_active=True).distinct()

        decision_item_ids = request.POST.getlist('decision_item')
        selected_decision_items = deliverable.decisionitem_set.filter(id__in=decision_item_ids)

        if form.is_valid() and selected_stakeholders.exists() and selected_decision_items.exists():
            form.instance.deliverable = deliverable
            form.instance.created_by = request.user
            meeting = form.save()

            for stakeholder in selected_stakeholders:
                meeting_stakeholder = MeetingStakeholder()
                meeting_stakeholder.meeting = meeting
                meeting_stakeholder.stakeholder = stakeholder
                meeting_stakeholder.save()

            for decision_item in selected_decision_items:
                meeting_item = MeetingItem()
                meeting_item.meeting = meeting
                meeting_item.decision_item = decision_item
                meeting_item.save()

            deliverable.save()
            messages.success(request, u'The meeting {0} was created successfully.'.format(meeting.name))
            return redirect(reverse('deliverables:meetings:meeting', args=(deliverable.pk, meeting.pk,)))
        else:
            messages.error(request, u'Please correct the error below.')
    else:
        form = MeetingForm()
        meeting_stakeholders = deliverable.stakeholders.filter(is_active=True).order_by('first_name', 'last_name', 'username')
        selected_stakeholders = meeting_stakeholders
        selected_decision_items = decision_items
    available_stakeholders = User.objects \
            .exclude(id__in=deliverable.stakeholders.all()) \
            .exclude(id__in=selected_stakeholders) \
            .filter(is_active=True) \
            .order_by('first_name', 'last_name', 'username')
    return render(request, 'deliverables/meetings/new.html', { 
        'deliverable': deliverable,
        'decision_items_fields': decision_items_fields,
        'decision_items': decision_items,
        'selected_decision_items': selected_decision_items,
        'form': form,
        'meeting_stakeholders': meeting_stakeholders,
        'available_stakeholders': available_stakeholders,
        'selected_stakeholders': selected_stakeholders
        })

@login_required
def meeting(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    meeting.calculate_all_rankings()
    stakeholders = [meeting_stakeholder.stakeholder for meeting_stakeholder in meeting.meetingstakeholder_set.select_related('stakeholder')]
    return render(request, 'deliverables/meetings/meeting.html', { 'meeting': meeting, 'stakeholders': stakeholders })

@login_required
@user_passes_test(lambda user: user.is_superuser)
@require_POST
def close_meeting(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    meeting.status = Meeting.CLOSED
    meeting.save()
    messages.success(request, u'The meeting {0} was closed successfully.'.format(meeting.name))
    return redirect(reverse('deliverables:deliverable', args=(meeting.deliverable.pk,)))

@login_required
def evaluate(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    factors = Factor.list().select_related('measure')

    measure_values = factors[0].measure.measurevalue_set.all()

    count = measure_values.count()
    if count > 0:
        size = 75.0/count
        relative_col_size = '{0}%'.format(size)
    else:
        relative_col_size = 'auto'

    evaluations = Evaluation.get_user_evaluations_by_meeting(user=request.user, meeting=meeting) \
            .select_related('meeting', 'meeting_item', 'user', 'factor', 'factor__measure', 'measure', 'measure_value', 'rationale')
    meeting_items = meeting.meetingitem_set.select_related('decision_item').all()
    total_items = meeting_items.count()
    search_query = request.GET.get('search')
    if search_query:
        meeting_items = meeting_items.filter(decision_item__name__icontains=search_query)
    return render(request, 'deliverables/meetings/evaluate.html', { 
        'meeting' : meeting, 
        'factors' : factors,
        'measure_values': measure_values,
        'relative_col_size': relative_col_size,
        'evaluations' : evaluations,
        'total_items': total_items,
        'meeting_items': meeting_items,
        'search_query': search_query
        })

@login_required
@require_POST
def save_evaluation(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)

    meeting_item_id = request.POST.get('meeting_item_id')
    factor_id = request.POST.get('factor_id')
    measure_id = request.POST.get('measure_id')
    measure_value_id = request.POST.get('measure_value_id')

    meeting_item = MeetingItem.objects.get(pk=meeting_item_id)
    factor = Factor.objects.get(pk=factor_id)
    measure = Measure.objects.get(pk=measure_id)

    if measure_value_id:
        measure_value = MeasureValue.objects.get(pk=measure_value_id)
    else:
        measure_value = None

    Evaluation.objects.update_or_create(
            meeting=meeting, 
            meeting_item=meeting_item, 
            user=request.user, 
            factor=factor, 
            measure=measure,
            defaults={ 'evaluated_at': timezone.now(), 'measure_value': measure_value }
    )

    meeting.deliverable.save()

    return HttpResponse()

@login_required
@require_POST
def save_rationale(request, deliverable_id, meeting_id):
    try:
        meeting = Meeting.objects.get(pk=meeting_id, deliverable__id=deliverable_id)

        meeting_item_id = request.POST.get('meeting_item_id')
        factor_id = request.POST.get('factor_id')
        measure_id = request.POST.get('measure_id')

        meeting_item = MeetingItem.objects.get(pk=meeting_item_id)
        factor = Factor.objects.get(pk=factor_id)
        measure = Measure.objects.get(pk=measure_id)

        evaluation, created = Evaluation.objects.get_or_create(
                meeting=meeting, 
                user=request.user, 
                meeting_item=meeting_item, 
                factor=factor, 
                measure=measure
        )
        
        if evaluation.rationale:
            form = RationaleForm(request.POST, instance=evaluation.rationale)
        else:
            form = RationaleForm(request.POST)
            form.instance.user = request.user

        if form.is_valid():
            evaluation.rationale = form.save()
            evaluation.save()
            meeting.deliverable.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest(form['text'].errors.as_text())

    except ObjectDoesNotExist:
        return HttpResponseBadRequest('An error ocurred while trying to save your data.')

@login_required
def dashboard(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    chart = Highcharts()
    
    charts = []
    charts.append({ 'chart_id': 'factors_usage',  'chart_title': 'Factors Usage', 'chart_uri': reverse('deliverables:meetings:dashboard_factors_usage_chart', args=(deliverable_id, meeting_id,)) })
    charts.append({ 'chart_id': 'stakeholders_input', 'chart_title': 'Stakeholders Input', 'chart_uri': reverse('deliverables:meetings:dashboard_stakeholders_input_chart', args=(deliverable_id, meeting_id,)) })

    return render(request, 'deliverables/meetings/dashboard/dashboard.html', { 
        'meeting' : meeting,
        'charts' : charts,
        'chart_menu_active': 'overview'
        })

@login_required
def dashboard_factors_usage_chart(request, deliverable_id, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id)
    chart = Highcharts()
    options = chart.factors_usage_bar_chart(meeting)
    dump = json.dumps(options)
    return HttpResponse(dump, content_type='application/json')

@login_required
def dashboard_stakeholders_input_chart(request, deliverable_id, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id)
    chart = Highcharts()
    options = chart.stakeholders_input_bar_chart(meeting)
    dump = json.dumps(options)
    return HttpResponse(dump, content_type='application/json')

@login_required
def features(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    charts = meeting.meetingitem_set.all()
    return render(request, 'deliverables/meetings/dashboard/features.html', { 
        'meeting' : meeting,
        'charts' : charts,
        'chart_uri': 'features',
        'chart_menu_active' : 'features',
        'chart_page_title' : 'Features Selection'
        })

@login_required
def features_chart(request, deliverable_id, meeting_id, meeting_item_id):
    chart_type = request.GET.get('chart')
    chart = Highcharts()
    options = chart.features_selection_stacked_chart(meeting_id, meeting_item_id, chart_type)
    dump = json.dumps(options)
    return HttpResponse(dump, content_type='application/json')


@login_required
def features_acceptance(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    charts = meeting.meetingitem_set.all()
    return render(request, 'deliverables/meetings/dashboard/features_acceptance.html', { 
        'meeting' : meeting,
        'charts' : charts,
        'chart_uri': 'features-acceptance',
        'chart_menu_active' : 'features_acceptance',
        'chart_page_title' : 'Features Acceptance'
        })

@login_required
def features_acceptance_chart(request, deliverable_id, meeting_id, meeting_item_id):
    chart_type = request.GET.get('chart', 'simple')
    chart = Highcharts()

    options = {}

    if chart_type == 'simple': 
        options = chart.features_acceptance_simple_treemap(meeting_id, meeting_item_id)
    elif chart_type == 'detailed':
        options = chart.features_acceptance_detailed_treemap(meeting_id, meeting_item_id)
    elif chart_type == 'bubble':
        options = chart.features_acceptance_bubbles(meeting_id, meeting_item_id)
    else:
        options = chart.features_acceptance_pie_chart_drilldown(meeting_id, meeting_item_id)

    dump = json.dumps(options)
    return HttpResponse(dump, content_type='application/json')

@login_required
def decision_items_overview(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    chart_type = request.GET.get('chart')
    chart = Highcharts()
    options = chart.decision_items_overview(meeting, chart_type)
    dump = json.dumps(options)

    if 'application/json' in request.META.get('HTTP_ACCEPT'):
        return HttpResponse(dump, content_type='application/json')
    else:
        return render(request, 'deliverables/meetings/dashboard/decision_items_overview.html', { 
            'meeting' : meeting, 
            'dump' : dump,
            'chart_uri': 'decision-items-overview',
            'chart_menu_active': 'decision_items_overview',
            'chart_page_title': 'Decision Items Overview'
            })

@login_required
def features_comparison(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    evaluations = Evaluation.get_evaluations_by_meeting(meeting)
    measure = evaluations[0].measure
    charts = measure.measurevalue_set.all()
    return render(request, 'deliverables/meetings/dashboard/measure_values_charts.html', { 
        'meeting' : meeting, 
        'charts' : charts,
        'chart_uri': 'features-comparison',
        'chart_menu_active': 'features_comparison',
        'chart_page_title': 'Features Comparison'
        })

@login_required
def features_comparison_chart(request, deliverable_id, meeting_id, measure_value_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    measure_value = MeasureValue.objects.get(pk=measure_value_id)
    chart = Highcharts()
    options = chart.feature_comparison_bar_chart(meeting, measure_value)
    dump = json.dumps(options)

    if 'application/json' in request.META.get('HTTP_ACCEPT'):
        return HttpResponse(dump, content_type='application/json')
    else:
        return render(request, 'deliverables/meetings/dashboard/generic_chart.html', { 
            'meeting' : meeting, 
            'dump' : dump,
            'chart_uri': 'features-comparison',
            'chart_menu_active': 'features_comparison',
            'chart_page_title': 'Features Comparison'
            })
