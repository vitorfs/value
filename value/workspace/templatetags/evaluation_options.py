from django import template

register = template.Library()

def checksign(is_checked):
    sign = '<span class="glyphicon glyphicon-unchecked"></span>'
    if is_checked:
        sign = '<span class="glyphicon glyphicon-check"></span>'
    return sign

def background(is_checked, color):
    if is_checked:
        return 'style="background-color: ' + color + '"'
    return ''

def selected(is_evaluated):
    if is_evaluated:
        return ' class="selected"'
    return ''

@register.simple_tag
def evaluation_options(evaluations, item, factor):

    is_evaluated = False
    for evaluation in evaluations:
        if item.pk == evaluation.item.pk and factor.pk == evaluation.factor.pk:
            is_evaluated = True

    html = '<tr{0}><td>{1}</td>'.format(selected(is_evaluated), factor.name)

    for measure_value in factor.measure.get_values():
        is_checked = False
        for evaluation in evaluations:
            if evaluation.measure_value:
                if evaluation.instance.pk == item.instance.pk and evaluation.item.pk == item.pk and evaluation.factor.pk == factor.pk and evaluation.measure.pk == factor.measure.pk and evaluation.measure_value.pk == measure_value.pk:
                    is_checked = True
        html += '''<td class="text-center evaluable" 
data-color="{0}" 
data-instance-id="{1}" 
data-item-id="{2}"
data-factor-id="{3}" 
data-measure-id="{4}" 
data-measure-value-id="{5}"
{6}>
{7}
</td>'''.format(measure_value.color, item.instance.pk, item.pk, factor.pk, factor.measure.pk, measure_value.pk, background(is_checked, measure_value.color), checksign(is_checked))

    is_none = False
    for evaluation in evaluations:
        if evaluation.instance.pk == item.instance.pk and evaluation.item.pk == item.pk and evaluation.factor.pk == factor.pk and evaluation.measure_value == None:
            is_none = True

    html += '''<td class="text-center evaluable" 
data-color="#E7E7E7"
data-instance-id="{0}"
data-item-id="{1}"
data-factor-id="{2}"
data-measure-id="{3}"
data-measure-value-id=""
{4}>
{5}
</td>'''.format(item.instance.pk, item.pk, factor.pk, factor.measure.pk, background(is_none, '#E7E7E7'), checksign(is_none))

    html += '</tr>'

    return html
