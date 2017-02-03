from django import template

register = template.Library()


@register.filter('matrix_cell_color')
def matrix_cell_color(percentage):
    '''
     0 -  20: #961512 (strong red)
    20 -  40: #D9534F (light red)
    40 -  60: #F0AD4E (yellow)
    60 -  80: #5CB85C (light green)
    80 - 100: #1B7C1B (strong green)
    '''
    if percentage < 20:
        color = '#961512'
    elif percentage >= 20 and percentage < 40:
        color = '#D9534F'
    elif percentage >= 40 and percentage < 60:
        color = '#F0AD4E'
    elif percentage >= 60 and percentage < 80:
        color = '#5CB85C'
    else:
        color = '#1B7C1B'
    return color