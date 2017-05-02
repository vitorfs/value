import json

from django.http import HttpResponse
from django.shortcuts import render

from value.deliverables.meetings.models import Meeting, MeetingItem
from value.deliverables.meetings.utils import format_percentage
from value.deliverables.meetings.charts import Highcharts


def index(request):
    return HttpResponse('VALUE API')


def value_summary(request):
    try:
        issue_id = request.GET.get('id')
        item = MeetingItem.objects.filter(decision_item__name=issue_id).order_by('-meeting').first()
        '''
        summary = item.evaluation_summary \
            .values('percentage_votes', 'measure_value__description', 'measure_value__color')


        total = 0
        inner = ''
        for ranking in summary:
            total += ranking['percentage_votes']
            inner += u'<td style="background-color:{0};color:#fff;width:{1}%">{1}</td>'.format(
                ranking['measure_value__color'],
                format_percentage(ranking['percentage_votes'])
            )

        output = u'<table style="width:100%"><tbody><tr>{0}</tr></tbody></table>'.format(inner)
        return HttpResponse(output)

        '''

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
        else:
            meeting = Meeting.objects.get(pk=issue_id)
            if chart_type == 'decision_items_overview':
                stakeholder_ids = meeting.meetingstakeholder_set.values_list('stakeholder', flat=True)
                options = charts.decision_items_overview(meeting, 'stacked_columns', stakeholder_ids)
                dump = json.dumps(options)
            else:
                options = charts.value_ranking(meeting)
                dump = json.dumps(options)

        return render(request, 'api/chart.html', {'dump': dump})
    except Exception, e:
        return HttpResponse('It was not possible to load the chart.')

