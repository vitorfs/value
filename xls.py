from xlrd import open_workbook

filename = '/Users/vitorfs/Downloads/Internal_Product_Plan_template_ValueProject.xlsx'
wb = open_workbook(filename)
print wb

for sheet in wb.sheets():
    print sheet.number
    print sheet.nrows
    for row in range(sheet.nrows):
        data = u''
        for col in range(sheet.ncols):
            data += str(row) + ':' + str(col) + ' ' + str(sheet.cell(row, col).value) + ', '
        print data