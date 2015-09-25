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

def get_stakeholders_ids(meeting, ids=None):
    stakeholder_ids = meeting.meetingstakeholder_set.all().values_list('stakeholder__id', flat=True)
    if ids:
        try:
            stakeholder_ids = map(int, ids)
        except:
            pass
    return stakeholder_ids
