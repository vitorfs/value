# coding: utf-8

from string import ascii_uppercase

from django import template
from django.utils.html import mark_safe

register = template.Library()

@register.simple_tag
def excel_columns(name, index, settings):
    select = '<select id="id_column_{0}" name="column_{0}" class="form-control" {1}>{2}</select>'
    option = '<option value="{0}"{1}>{0}</option>'

    selected = ''
    if 'EXCEL_ENTRY_ORIENTATION' in settings.keys():
        if settings['EXCEL_ENTRY_ORIENTATION'] == 'row':
            if name in settings['EXCEL_IMPORT_TEMPLATE'].keys():
                selected = settings['EXCEL_IMPORT_TEMPLATE'][name]

    options = ''
    is_selected = False

    for c in ascii_uppercase:
        txt_selected = ''
        if c == selected:
            txt_selected = ' selected'
            is_selected = True
        options += option.format(c, txt_selected)

    for c in ascii_uppercase:
        c = 'A{0}'.format(c)
        txt_selected = ''
        if c == selected:
            txt_selected = ' selected'
            is_selected = True
        options += option.format(c, txt_selected)

    for c in ascii_uppercase:
        c = 'B{0}'.format(c)
        txt_selected = ''
        if c == selected:
            txt_selected = ' selected'
            is_selected = True
        options += option.format(c, txt_selected)

    if is_selected:
        html = select.format(name, '', options)
    else:
        html = select.format(name, 'disabled', options)

    return mark_safe(html)

@register.simple_tag
def excel_is_checked(name, settings):
    checked = ''
    if settings['EXCEL_ENTRY_ORIENTATION'] == 'row':
        if name in settings['EXCEL_IMPORT_TEMPLATE'].keys():
            checked = ' checked'
    return checked

@register.simple_tag
def excel_rows(name, index, settings):
    select = '<select id="id_row_{0}" name="row_{0}" class="form-control">{1}</select>'
    option = '<option value="{0}"{1}>{0}</option>'

    selected = ''
    if 'EXCEL_ENTRY_ORIENTATION' in settings.keys():
        if settings['EXCEL_ENTRY_ORIENTATION'] == 'column':
            if name in settings['EXCEL_IMPORT_TEMPLATE'].keys():
                selected = settings['EXCEL_IMPORT_TEMPLATE'][name]
    else:
        selected = index

    options = ''
    for c in range(1, 101):
        txt_selected = ''
        if str(c) == selected:
            txt_selected = ' selected'
        options += option.format(c, txt_selected)

    return mark_safe(select.format(name, options))
