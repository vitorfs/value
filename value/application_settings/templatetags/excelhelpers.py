from django import template
from string import ascii_uppercase

register = template.Library()

@register.simple_tag
def excel_columns(name, selected=''):
    select = '<select id="id_column_{0}" name="column_{0}" class="form-control">{1}</select>'
    option = '<option value="{0}"{1}>{0}</option>'

    options = ''
    for c in ascii_uppercase:
        txt_selected = ''
        if c == selected:
            txt_selected = ' selected'
        options += option.format(c, txt_selected)
    for c in ascii_uppercase:
        c = 'A{0}'.format(c)
        txt_selected = ''
        if c == selected:
            txt_selected = ' selected'
        options += option.format(c, txt_selected)
    for c in ascii_uppercase:
        c = 'B{0}'.format(c)
        txt_selected = ''
        if c == selected:
            txt_selected = ' selected'
        options += option.format(c, txt_selected)

    return select.format(name, options)

@register.simple_tag
def excel_rows(name, selected=''):
    select = '<select id="id_row_{0}" name="row_{0}" class="form-control">{1}</select>'
    option = '<option value="{0}"{1}>{0}</option>'

    options = ''
    for c in range(1, 101):
        txt_selected = ''
        if c == selected:
            txt_selected = ' selected'
        options += option.format(c, txt_selected)

    return select.format(name, options)
