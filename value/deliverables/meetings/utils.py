# coding: utf-8

from collections import OrderedDict

from value.deliverables.models import DecisionItemLookup


def get_or_set_order_session(request, meeting, cookie_name, db_model_order):
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
        charts_order[measure_value.pk] = measure_value.description

    for field_key, field_value in DecisionItemLookup.get_visible_fields().iteritems():
        charts_order[u'decision_item__{0}'.format(field_key)] = field_value['label']

    return charts_order

def get_or_set_charts_order_session(request, meeting, cookie_name):
    db_model_order = map(lambda key: u'decision_item__{0}'.format(key), DecisionItemLookup.get_visible_fields().keys())
    return get_or_set_order_session(request, meeting, cookie_name, db_model_order)

def get_or_set_scenario_chars_order_session(request, meeting, cookie_name):
    db_model_order = ['name',]
    return get_or_set_order_session(request, meeting, cookie_name, db_model_order)

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
