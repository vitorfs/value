from django import template
register = template.Library()

@register.filter('relative_col_size')
def relative_col_size(list):
    length = len(list)
    if length > 0:
        size = 75.0/length
        return '{0}%'.format(size)
    return ''