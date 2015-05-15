import calendar
from django import template

register = template.Library()

def get_calendar(year, month):
    blank_week = [0, 0, 0, 0, 0, 0, 0]
    calendar.setfirstweekday(calendar.SUNDAY)
    c = calendar.monthcalendar(year, month)
    if len(c) == 4:
        c.append(blank_week)
    if len(c) == 5:
        c.append(blank_week)
    return c    

@register.simple_tag
def month_calendar(year, month):
    calendar.setfirstweekday(calendar.SUNDAY)
    month_calendar = calendar.monthcalendar(year, month)
    html = '<h4>{0}</h4>'.format(calendar.month_name[month])
    html += '<table class="table table-calendar">'
    html += '<thead><tr><th>S</th><th>M</th><th>T</th><th>W</th><th>T</th><th>F</th><th>S</th></tr></thead>'
    html += '<tbody>'
    for week in month_calendar:
        html += '<tr>'
        for day in week:
            if day == 0:
                day = ''
            html += '<td>{0}</td>'.format(day)
        html += '</tr>'
    html += '</tbody></table>'
    return html