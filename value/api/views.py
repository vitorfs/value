import json

from django.http import HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse

from value.deliverables.meetings.models import Meeting, MeetingItem
from value.deliverables.meetings.utils import format_percentage
from value.deliverables.meetings.charts import Highcharts


def index(request):
    return HttpResponse('VALUE API')


def value_summary(request):
    try:
        issue_id = request.GET.get('id')
        item = MeetingItem.objects.filter(decision_item__name=issue_id).order_by('-meeting').first()
        return render(request, 'api/summary.html', {'item': item})
    except:
        return HttpResponse(u'Issue not found.')


def charts(request):
    try:
        issue_id = request.GET.get('id')
        chart_type = request.GET.get('chartType')
        charts = Highcharts()
        if chart_type == 'factors_comparison':
            item = MeetingItem.objects.filter(decision_item__name=issue_id).order_by('-meeting').first()
            stakeholder_ids = item.meeting.meetingstakeholder_set.values_list('stakeholder', flat=True)
            options = charts.factors_comparison(item.meeting_id, item.pk, 'stacked_bars', stakeholder_ids)
            dump = json.dumps(options)
            url = request.build_absolute_uri(
                reverse('deliverables:meetings:features', args=(
                    item.meeting.deliverable_id,
                    item.meeting_id
                ))
            )
        else:
            meeting = Meeting.objects.get(pk=issue_id)
            if chart_type == 'decision_items_overview':
                stakeholder_ids = meeting.meetingstakeholder_set.values_list('stakeholder', flat=True)
                options = charts.decision_items_overview(meeting, 'stacked_columns', stakeholder_ids)
                dump = json.dumps(options)
                url = request.build_absolute_uri(
                    reverse('deliverables:meetings:decision_items_overview', args=(meeting.deliverable_id, meeting.pk, ))
                )
            else:
                options = charts.value_ranking(meeting)
                dump = json.dumps(options)
                url = request.build_absolute_uri(
                    reverse('deliverables:meetings:value_ranking', args=(meeting.deliverable_id, meeting.pk, ))
                )

        return render(request, 'api/chart.html', {
            'dump': dump,
            'url': url
        })
    except Exception, e:
        return HttpResponse('It was not possible to load the chart.')

