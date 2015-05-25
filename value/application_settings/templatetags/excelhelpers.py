from string import ascii_uppercase
from django import template

register = template.Library()

@register.simple_tag
def excel_columns(name, index, settings):
    select = '<select id="id_column_{0}" name="column_{0}" class="form-control">{1}</select>'
    option = '<option value="{0}"{1}>{0}</option>'

    if settings['EXCEL_ENTRY_ORIENTATION'] == 'row':
        selected = settings['EXCEL_IMPORT_TEMPLATE'][name]
    else:
        selected = index

    options = ''
    i = 0
    for c in ascii_uppercase:
        i = i + 1
        txt_selected = ''
        if c == selected or i == index:
            txt_selected = ' selected'
        options += option.format(c, txt_selected)
    for c in ascii_uppercase:
        i = i + 1
        c = 'A{0}'.format(c)
        txt_selected = ''
        if c == selected or i == index:
            txt_selected = ' selected'
        options += option.format(c, txt_selected)
    for c in ascii_uppercase:
        i = i + 1
        c = 'B{0}'.format(c)
        txt_selected = ''
        if c == selected or i == index:
            txt_selected = ' selected'
        options += option.format(c, txt_selected)

    return select.format(name, options)

@register.simple_tag
def excel_rows(name, index, settings):
    select = '<select id="id_row_{0}" name="row_{0}" class="form-control">{1}</select>'
    option = '<option value="{0}"{1}>{0}</option>'

    if settings['EXCEL_ENTRY_ORIENTATION'] == 'column':
        selected = settings['EXCEL_IMPORT_TEMPLATE'][name]
    else:
        selected = index

    options = ''
    for c in range(1, 101):
        txt_selected = ''
        if str(c) == selected:
            txt_selected = ' selected'
        options += option.format(c, txt_selected)

    return select.format(name, options)
