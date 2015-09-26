# coding: utf-8

def get_or_set_order_session(request, meeting, cookie_name, valid_orders):
    order = '-value_ranking'
    valid_measures = map(str, meeting.deliverable.measure.measurevalue_set.values_list('id', flat=True))
    valid_orders += valid_measures
    if 'order' in request.GET:
        order = request.GET.get('order')
    elif cookie_name in request.session:
        order = request.session.get(cookie_name)
    if order not in valid_orders:
        order = '-value_ranking'
    request.session[cookie_name] = order
    return order

def get_or_set_charts_order_session(request, meeting, cookie_name):
    valid_orders = ['decision_item__name', '-value_ranking']
    return get_or_set_order_session(request, meeting, cookie_name, valid_orders)

def get_or_set_scenario_chars_order_session(request, meeting, cookie_name):
    valid_orders = ['name', '-value_ranking']
    return get_or_set_order_session(request, meeting, cookie_name, valid_orders)

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
