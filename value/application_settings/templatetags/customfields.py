from django import template
from value.deliverables.models import DecisionItemLookup

register = template.Library()


@register.simple_tag
def custom_field_attr(fields, column, attr):
    try:
        return fields['column_{0}'.format(column)][attr]
    except:
        return ''


@register.simple_tag
def custom_field_display(fields, column):
    column_key = 'column_{0}'.format(column)
    if column_key in fields.keys():
        if fields[column_key]['display']:
            return 'checked'
    return ''


@register.simple_tag
def custom_field_is_active(fields, column):
    if 'column_{0}'.format(column) in fields.keys():
        return 'checked'
    else:
        return ''


@register.simple_tag
def custom_field_selected(fields, column, field_type):
    key = 'column_{0}'.format(column)
    if key in fields.keys():
        if fields[key]['type'] == field_type[0]:
            return 'selected'
    else:
        return ''


@register.simple_tag
def custom_field_sort_icon(field, order):
    template = '<span class="fa fa-sort-{0}-{1}"></span>'
    if field['type'] == DecisionItemLookup.STRING:
        icon = 'alpha'
    else:
        icon = 'numeric'
    return template.format(icon, order)
