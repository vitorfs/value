from django import template

register = template.Library()

@register.simple_tag
def custom_field_attr(fields, column, attr):
    try:
        return fields['column_{0}'.format(column)][attr]
    except Exception, e:
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
