# coding: utf-8

def get_or_set_charts_order_session(request, cookie_name, default_order, valid_orders):
    order = default_order
    if 'order' in request.GET:
        order = request.GET.get('order')
    elif cookie_name in request.session:
        order = request.session.get(cookie_name)
    if order not in valid_orders:
        order = default_order
    request.session[cookie_name] = order
    return order

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
