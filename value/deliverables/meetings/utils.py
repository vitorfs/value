# coding: utf-8

from collections import OrderedDict

from value.deliverables.models import DecisionItemLookup


def get_bar_chart_types_dict():
    chart_types = OrderedDict()
    chart_types['stacked_bars'] = { 'label': 'Stacked Bars', 'icon': 'glyphicon glyphicon-align-left' }
    chart_types['basic_bars'] = { 'label': 'Basic Bars', 'icon': 'glyphicon glyphicon-align-left' }
    chart_types['stacked_columns'] = { 'label': 'Stacked Columns', 'icon': 'glyphicon glyphicon-signal' }
    chart_types['basic_columns'] = { 'label': 'Basic Columns', 'icon': 'glyphicon glyphicon-signal' }
    return chart_types

def get_treemap_chart_types_dict():
    chart_types = OrderedDict()
    chart_types['simple'] = { 'label': 'Simple Treemap', 'icon': 'fa fa-th-large' }
    chart_types['detailed'] = { 'label': 'Detailed Treemap', 'icon': 'fa fa-th' }
    chart_types['pie'] = { 'label': 'Detailed Pie Chart', 'icon': 'fa fa-pie-chart' }
    return chart_types

def _get_or_set_chart_session(request, cookie_name, default_chart_type, chart_types):
    chart_type = default_chart_type
    if 'chart_type' in request.GET:
        chart_type = request.GET.get('chart_type')
    elif cookie_name in request.session:
        chart_type = request.session.get(cookie_name)
    if chart_type not in chart_types:
        chart_type = default_chart_type
    request.session[cookie_name] = chart_type
    return chart_type

def get_or_set_bar_chart_type_session(request, cookie_name, default_chart_type='stacked_bars'):
    return _get_or_set_chart_session(request, cookie_name, default_chart_type, get_bar_chart_types_dict().keys())

def get_or_set_treemap_chart_type_session(request, cookie_name, default_chart_type='simple'):
    return _get_or_set_chart_session(request, cookie_name, default_chart_type, get_treemap_chart_types_dict().keys())

def _get_or_set_order_session(request, meeting, cookie_name, db_model_order):
    order = '-value_ranking'
    db_model_order.append('-value_ranking')
    ranking_order = map(str, meeting.deliverable.measure.measurevalue_set.values_list('id', flat=True))
    valid_orders = db_model_order + ranking_order
    if 'order' in request.GET:
        order = request.GET.get('order')
    elif cookie_name in request.session:
        order = request.session.get(cookie_name)
    if order not in valid_orders:
        order = '-value_ranking'
    request.session[cookie_name] = order
    return order

def get_charts_order_dict(measure):
    charts_order = OrderedDict()
    charts_order['-value_ranking'] = 'Value Ranking'

    for measure_value in measure.measurevalue_set.all():
        charts_order[measure_value.pk] = u'{0} {1}'.format(measure_value.description, measure_value.measure.name)

    for field_key, field_value in DecisionItemLookup.get_visible_fields().iteritems():
        charts_order[u'decision_item__{0}'.format(field_key)] = field_value['label']

    return charts_order

def get_scenario_charts_order_dict(measure):
    charts_order = OrderedDict()
    charts_order['-value_ranking'] = 'Value Ranking'

    for measure_value in measure.measurevalue_set.all():
        charts_order[measure_value.pk] = u'{0} {1}'.format(measure_value.description, measure_value.measure.name)

    charts_order['name'] = 'Name'

    return charts_order

def get_or_set_charts_order_session(request, meeting, cookie_name):
    db_model_order = map(lambda key: u'decision_item__{0}'.format(key), DecisionItemLookup.get_visible_fields().keys())
    return _get_or_set_order_session(request, meeting, cookie_name, db_model_order)

def get_or_set_scenario_charts_order_session(request, meeting, cookie_name):
    db_model_order = ['name',]
    return _get_or_set_order_session(request, meeting, cookie_name, db_model_order)

def get_stakeholders_ids(meeting, stakeholders=None):
    stakeholder_ids = list(meeting.meetingstakeholder_set.all().values_list('stakeholder__id', flat=True))
    if hasattr(stakeholders, '__iter__'):
        try:
            stakeholder_ids = map(int, stakeholders)
        except:
            stakeholder_ids = list()
    return stakeholder_ids

def format_percentage(raw_value):
    rounded_value = round(raw_value, 2)
    return '{:2.2f}'.format(rounded_value)

def get_votes_percentage(max_value, value, round_value=True):
    percentage = 0.0
    if max_value != 0:
        percentage = (value / float(max_value)) * 100.0
        if round_value:
            percentage = round(percentage, 2)
    return percentage
