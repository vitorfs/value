from django import template

register = template.Library()

@register.filter('attr')
def attr(obj, attr_name):
    value = getattr(obj, attr_name)
    if value == None:
        value = ''
    return value
