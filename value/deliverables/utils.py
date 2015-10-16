# coding: utf-8

def excel_column_map():
    column_map = {}
    i = 0
    for c in ascii_uppercase:
        column_map[c] = i
        i = i + 1
    for c in ascii_uppercase:
        c = 'A{0}'.format(c)
        column_map[c] = i
        i = i + 1
    for c in ascii_uppercase:
        c = 'B{0}'.format(c)
        column_map[c] = i
        i = i + 1
    return column_map
