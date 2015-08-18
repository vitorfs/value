from reportlab.graphics import renderPDF
import xml.dom.minidom
import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q
from django.db import transaction
from django.forms.models import modelformset_factory

from value.utils.svglib import SvgRenderer
from value.factors.models import Factor
from value.measures.models import Measure, MeasureValue
from value.deliverables.models import Deliverable, DecisionItemLookup, Rationale, DecisionItem
from value.deliverables.forms import RationaleForm
from value.deliverables.meetings.models import Meeting, MeetingItem, MeetingStakeholder, Evaluation
from value.deliverables.meetings.charts import Highcharts
from value.deliverables.meetings.forms import MeetingForm, MeetingItemFinalDecisionForm


@login_required
def index(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    return render(request, 'deliverables/meetings.html', { 'deliverable': deliverable })

@login_required
def new(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    decision_items_fields = DecisionItemLookup.get_visible_fields()
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
    return render(request, 'meetings/new.html', { 
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
    return redirect(reverse('deliverables:meetings:evaluate', args=(deliverable_id, meeting_id)))

@login_required
@user_passes_test(lambda user: user.is_superuser)
@require_POST
def close_meeting(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    meeting.status = Meeting.CLOSED
    meeting.save()
    meeting.deliverable.save()
    messages.success(request, u'The meeting {0} was closed successfully.'.format(meeting.name))
    return redirect(reverse('deliverables:meetings:meeting', args=(meeting.deliverable.pk, meeting.pk)))

@login_required
@user_passes_test(lambda user: user.is_superuser)
@require_POST
def open_meeting(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    meeting.status = Meeting.ONGOING
    meeting.save()
    meeting.deliverable.save()
    messages.success(request, u'The meeting {0} was opened successfully.'.format(meeting.name))
    return redirect(reverse('deliverables:meetings:meeting', args=(meeting.deliverable.pk, meeting.pk)))

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
    return render(request, 'meetings/evaluate.html', { 
        'meeting': meeting, 
        'factors': factors,
        'measure_values': measure_values,
        'relative_col_size': relative_col_size,
        'evaluations': evaluations,
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

    meeting_item.calculate_ranking()
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
    charts.append({ 'chart_id': 'factors_usage', 'chart_title': 'Factors Usage', 'chart_uri': reverse('deliverables:meetings:dashboard_factors_usage_chart', args=(deliverable_id, meeting_id,)) })
    charts.append({ 'chart_id': 'stakeholders_input', 'chart_title': 'Stakeholders Input', 'chart_uri': reverse('deliverables:meetings:dashboard_stakeholders_input_chart', args=(deliverable_id, meeting_id,)) })

    return render(request, 'meetings/dashboard/dashboard_list.html', { 
        'meeting': meeting,
        'charts': charts,
        'chart_menu_active': 'overview'
        })

@login_required
def dashboard_factors_usage_chart(request, deliverable_id, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id)
    chart = Highcharts()
    options = chart.factors_usage_bar_chart(meeting)
    dump = json.dumps(options)
    chart_data = { 'chart_id': 'factors_usage', 'chart_title': 'Factors Usage', 'chart_uri': reverse('deliverables:meetings:dashboard_factors_usage_chart', args=(deliverable_id, meeting_id,)) }
    if 'application/json' in request.META.get('HTTP_ACCEPT'):
        return HttpResponse(dump, content_type='application/json')
    else:
        return render(request, 'meetings/dashboard/dashboard_popup.html', { 
            'meeting': meeting,
            'chart': chart_data,
            'dump': dump
            })

@login_required
def dashboard_stakeholders_input_chart(request, deliverable_id, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id)
    chart = Highcharts()
    options = chart.stakeholders_input_bar_chart(meeting)
    dump = json.dumps(options)
    chart_data = { 'chart_id': 'stakeholders_input', 'chart_title': 'Stakeholders Input', 'chart_uri': reverse('deliverables:meetings:dashboard_stakeholders_input_chart', args=(deliverable_id, meeting_id,)) }
    if 'application/json' in request.META.get('HTTP_ACCEPT'):
        return HttpResponse(dump, content_type='application/json')
    else:
        return render(request, 'meetings/dashboard/dashboard_popup.html', { 
            'meeting': meeting,
            'chart': chart_data,
            'dump': dump
            })

@login_required
def features(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    charts = meeting.meetingitem_set.all()
    stakeholder_ids = [stakeholder.stakeholder.pk for stakeholder in meeting.meetingstakeholder_set.all()]
    return render(request, 'meetings/dashboard/features_list.html', { 
        'meeting': meeting,
        'charts': charts,
        'stakeholder_ids': stakeholder_ids,
        'chart_type': 'stacked_bars',
        'chart_uri': 'features',
        'chart_menu_active': 'features',
        'chart_page_title': 'Factors Comparison'
        })

@login_required
def features_chart(request, deliverable_id, meeting_id, meeting_item_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    meeting_item = meeting.meetingitem_set.get(pk=meeting_item_id)
    chart_type = request.GET.get('chart-type')
    stakeholder_ids = request.GET.getlist('stakeholder')
    try:
        stakeholder_ids = list(map(int, stakeholder_ids))
    except:
        pass
    chart = Highcharts()
    options = chart.features_selection_stacked_chart(meeting_id, meeting_item_id, chart_type, stakeholder_ids)
    dump = json.dumps(options)
    if 'application/json' in request.META.get('HTTP_ACCEPT'):
        return HttpResponse(dump, content_type='application/json')
    else:
        return render(request, 'meetings/dashboard/features_popup.html', { 
            'meeting': meeting,
            'chart': meeting_item,
            'chart_uri': 'features',
            'chart_type': chart_type,
            'stakeholder_ids': stakeholder_ids,
            'dump': dump
            })

@login_required
def features_acceptance(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    charts = meeting.meetingitem_set.all()
    stakeholder_ids = [stakeholder.stakeholder.pk for stakeholder in meeting.meetingstakeholder_set.all()]
    return render(request, 'meetings/dashboard/features_acceptance_list.html', { 
        'meeting': meeting,
        'charts': charts,
        'stakeholder_ids': stakeholder_ids,
        'chart_type': 'simple',
        'chart_uri': 'features-acceptance',
        'chart_menu_active': 'features_acceptance',
        'chart_page_title': 'Features Acceptance'
        })

@login_required
def features_acceptance_chart(request, deliverable_id, meeting_id, meeting_item_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    meeting_item = meeting.meetingitem_set.get(pk=meeting_item_id)
    chart_type = request.GET.get('chart-type', 'simple')
    stakeholder_ids = request.GET.getlist('stakeholder')
    try:
        stakeholder_ids = list(map(int, stakeholder_ids))
    except:
        pass
    chart = Highcharts()
    options = {}
    if chart_type == 'simple': 
        options = chart.features_acceptance_simple_treemap(meeting_id, meeting_item_id, stakeholder_ids)
    elif chart_type == 'detailed':
        options = chart.features_acceptance_detailed_treemap(meeting_id, meeting_item_id, stakeholder_ids)
    elif chart_type == 'bubble':
        options = chart.features_acceptance_bubbles(meeting_id, meeting_item_id, stakeholder_ids)
    else:
        options = chart.features_acceptance_pie_chart_drilldown(meeting_id, meeting_item_id, stakeholder_ids)
    dump = json.dumps(options)
    if 'application/json' in request.META.get('HTTP_ACCEPT'):
        return HttpResponse(dump, content_type='application/json')
    else:
        return render(request, 'meetings/dashboard/features_acceptance_popup.html', { 
            'meeting': meeting,
            'chart': meeting_item,
            'chart_uri': 'features-acceptance',
            'chart_type': chart_type,
            'stakeholder_ids': stakeholder_ids,
            'dump': dump
            })

@login_required
def decision_items_overview(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    chart_type = request.GET.get('chart-type', 'stacked_bars')
    chart = Highcharts()
    if 'stakeholder' in request.GET:
        stakeholder_ids = request.GET.getlist('stakeholder')
        try:
            stakeholder_ids = list(map(int, stakeholder_ids))
        except:
            pass
    else:
        stakeholder_ids = [stakeholder.stakeholder.pk for stakeholder in meeting.meetingstakeholder_set.all()]
    options = chart.decision_items_overview(meeting, chart_type, stakeholder_ids)
    dump = json.dumps(options)
    if 'application/json' in request.META.get('HTTP_ACCEPT'):
        return HttpResponse(dump, content_type='application/json')
    else:
        template_name = 'meetings/dashboard/decision_items_overview.html'
        if 'popup' in request.GET:
            template_name = 'meetings/dashboard/decision_items_overview_popup.html'
        return render(request, template_name, { 
            'meeting': meeting, 
            'dump': dump,
            'stakeholder_ids': stakeholder_ids,
            'chart_type': 'stacked_bars',
            'chart_uri': 'decision-items-overview',
            'chart_menu_active': 'decision_items_overview',
            'chart_page_title': 'Decision Items Overview'
            })

@login_required
def features_comparison(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    stakeholder_ids = [stakeholder.stakeholder.pk for stakeholder in meeting.meetingstakeholder_set.all()]
    evaluations = Evaluation.get_evaluations_by_meeting(meeting).filter(user_id__in=stakeholder_ids)
    measure = evaluations[0].measure
    charts = measure.measurevalue_set.all()
    return render(request, 'meetings/dashboard/decision_items_comparison_list.html', { 
        'meeting': meeting, 
        'charts': charts,
        'stakeholder_ids': stakeholder_ids,
        'chart_uri': 'features-comparison',
        'chart_menu_active': 'features_comparison',
        'chart_page_title': 'Features Comparison'
        })

@login_required
def features_comparison_chart(request, deliverable_id, meeting_id, measure_value_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    measure_value = MeasureValue.objects.get(pk=measure_value_id)
    stakeholder_ids = request.GET.getlist('stakeholder')
    try:
        stakeholder_ids = list(map(int, stakeholder_ids))
    except:
        pass
    chart = Highcharts()
    options = chart.feature_comparison_bar_chart(meeting, measure_value, stakeholder_ids)
    dump = json.dumps(options)
    chart_data = MeasureValue.objects.get(id=measure_value_id)
    if 'application/json' in request.META.get('HTTP_ACCEPT'):
        return HttpResponse(dump, content_type='application/json')
    else:
        return render(request, 'meetings/dashboard/decision_items_comparison_popup.html', { 
            'meeting': meeting, 
            'dump': dump,
            'chart': chart_data,
            'stakeholder_ids': stakeholder_ids,
            'chart_uri': 'features-comparison',
            'chart_menu_active': 'features_comparison',
            'chart_page_title': 'Features Comparison'
            })

@login_required
def factors_groups(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    charts = meeting.meetingitem_set.all()
    stakeholder_ids = [stakeholder.stakeholder.pk for stakeholder in meeting.meetingstakeholder_set.all()]
    return render(request, 'meetings/dashboard/factors_groups_list.html', { 
            'meeting': meeting,
            'charts': charts,
            'stakeholder_ids': stakeholder_ids,
            'chart_type': 'stacked_bars',
            'chart_uri': 'factors-groups-comparison',
            'chart_menu_active': 'factors_groups',
            'chart_page_title': 'Factors Groups Comparison'
            })

@login_required
def factors_groups_chart(request, deliverable_id, meeting_id, meeting_item_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    meeting_item = meeting.meetingitem_set.get(pk=meeting_item_id)
    stakeholder_ids = request.GET.getlist('stakeholder')
    try:
        stakeholder_ids = list(map(int, stakeholder_ids))
    except:
        pass
    chart = Highcharts()
    options = chart.factors_groups(meeting_item, stakeholder_ids)
    dump = json.dumps(options)
    if 'application/json' in request.META.get('HTTP_ACCEPT'):
        return HttpResponse(dump, content_type='application/json')
    else:
        return render(request, 'meetings/dashboard/factors_groups_popup.html', { 
            'meeting': meeting,
            'chart': meeting_item,
            'chart_uri': 'features',
            'stakeholder_ids': stakeholder_ids,
            'dump': dump
            })

@login_required
def value_ranking(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    chart = Highcharts()
    options = chart.value_ranking(meeting)
    dump = json.dumps(options)
    return render(request, 'meetings/dashboard/value_ranking.html', { 
            'meeting': meeting,
            'chart_page_title': 'Value Ranking',
            'chart_menu_active': 'value_ranking',
            'chart_uri': 'value-ranking',
            'dump': dump
            })

@login_required
def settings(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            meeting.deliverable.save()
            messages.success(request, u'The meeting details was saved successfully!')
        else:
            messages.error(request, u'Please correct the error below.')
    else:
        form = MeetingForm(instance=meeting)
    return render(request, 'meetings/settings/details.html', {
            'meeting': meeting,
            'form': form
            })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def decision_items(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    decision_items_in_use = meeting.meetingitem_set.values('decision_item__id')
    available_decision_items = meeting.deliverable.decisionitem_set.exclude(id__in=decision_items_in_use)
    return render(request, 'meetings/settings/items.html', { 
            'meeting': meeting, 
            'available_decision_items': available_decision_items
        })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def stakeholders(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    stakeholders = [meeting_stakeholder.stakeholder for meeting_stakeholder in meeting.meetingstakeholder_set.select_related('stakeholder')]
    available_stakeholders = User.objects \
            .exclude(id__in=meeting.meetingstakeholder_set.values('stakeholder__id')) \
            .filter(is_active=True) \
            .order_by('first_name', 'last_name', 'username')
    return render(request, 'meetings/settings/stakeholders.html', { 
            'meeting': meeting,
            'stakeholders': stakeholders,
            'available_stakeholders': available_stakeholders,
        })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def delete(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    if request.method == 'POST':
        meeting.delete()
        messages.success(request, u'The meeeting {0} was completly deleted successfully.'.format(meeting.name))
        return redirect(reverse('deliverables:deliverable', args=(meeting.deliverable.pk,)))
    else:
        return render(request, 'meetings/settings/delete.html', { 'meeting': meeting })

@login_required
def download(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    response = HttpResponse(content_type='application/pdf')
    try:
        svg = request.POST.get('svg')
        doc = xml.dom.minidom.parseString(svg.encode('utf-8'))
        svg = doc.documentElement
        svgRenderer = SvgRenderer()
        svgRenderer.render(svg)
        drawing = svgRenderer.finish()
        pdf = renderPDF.drawToString(drawing)
        response.write(pdf)     
    except:
        pass
    response['Content-Disposition'] = 'attachment; filename=dashboard.pdf'
    return response

@login_required
@require_POST
def remove_stakeholder(request, deliverable_id, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id, deliverable__id=deliverable_id)
    stakeholder_id = request.POST.get('stakeholder')
    user = User.objects.get(pk=stakeholder_id)
    if user != request.user:
        meeting_stakeholder = MeetingStakeholder.objects.get(stakeholder=user, meeting=meeting)
        meeting_stakeholder.delete()
        Evaluation.get_user_evaluations_by_meeting(user, meeting).delete()
        meeting.calculate_all_rankings()
        messages.success(request, u'{0} was successfully removed from the meeting!'.format(user.profile.get_display_name()))
    else:
        messages.warning(request, 'You cannot remove yourself from the meeting.')
    return redirect(reverse('deliverables:meetings:stakeholders', args=(deliverable_id, meeting_id)))

@login_required
@require_POST
@transaction.atomic
def add_stakeholders(request, deliverable_id, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id, deliverable__id=deliverable_id)
    stakeholder_ids = request.POST.getlist('stakeholders')
    if any(stakeholder_ids):
        for stakeholder_id in stakeholder_ids:
            user = User.objects.get(pk=stakeholder_id)
            meeting_stakeholder = MeetingStakeholder(stakeholder=user, meeting=meeting)
            meeting_stakeholder.save()
        meeting.calculate_all_rankings()
        messages.success(request, u'Stakeholders sucessfully added to the meeting!')
    else:
        messages.warning(request, u'Select at least one stakeholder to add.')
    return redirect(reverse('deliverables:meetings:stakeholders', args=(deliverable_id, meeting_id)))

@login_required
@require_POST
@transaction.atomic
def remove_decision_items(request, deliverable_id, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id, deliverable__id=deliverable_id)
    meeting_items_ids = request.POST.getlist('meeting_items')
    if any(meeting_items_ids):
        meeting.meetingitem_set.filter(id__in=meeting_items_ids).delete()
        meeting.calculate_all_rankings()
        messages.success(request, u'Decision items sucessfully removed from the meeting!')
    else:
        messages.warning(request, u'Select at least one decision item to remove.')
    return redirect(reverse('deliverables:meetings:decision_items', args=(deliverable_id, meeting_id)))

@login_required
@require_POST
@transaction.atomic
def add_decision_items(request, deliverable_id, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id, deliverable__id=deliverable_id)
    decision_items_ids = request.POST.getlist('decision_items')
    if any(decision_items_ids):
        for decision_item_id in decision_items_ids:
            decision_item = DecisionItem.objects.get(pk=decision_item_id)
            meeting_item = MeetingItem(meeting=meeting, decision_item=decision_item)
            meeting_item.save()
        meeting.calculate_all_rankings()
        messages.success(request, u'Decision items sucessfully added to the meeting!')
    else:
        messages.warning(request, u'Select at least one decision item to add.')
    return redirect(reverse('deliverables:meetings:decision_items', args=(deliverable_id, meeting_id)))

@login_required
def final_decision(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    meeting.calculate_all_rankings()

    MeetingItemFormset = modelformset_factory(MeetingItem, form=MeetingItemFinalDecisionForm, extra=0)
    meeting_items = meeting.meetingitem_set.select_related('decision_item').all()
    formset = MeetingItemFormset(queryset=meeting_items)

    return render(request, 'meetings/final_decision.html', { 
            'meeting': meeting,
            'formset': formset,
        })

@login_required
@require_POST
@transaction.atomic
def save_final_decision(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    MeetingItemFormset = modelformset_factory(MeetingItem, form=MeetingItemFinalDecisionForm, extra=0)
    formset = MeetingItemFormset(request.POST)

    errors = []
    for form in formset:
        if form.is_valid():
            form.save()
        else:
            errors.append(form.instance.pk)

    if any(errors):
        dump = json.dumps(errors)
        return HttpResponseBadRequest(dump, content_type='application/json')
    return HttpResponse()
        
