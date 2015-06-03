from django import template

register = template.Library()

def checksign(is_checked):
    sign = '<span class="glyphicon glyphicon-unchecked"></span>'
    if is_checked:
        sign = '<span class="glyphicon glyphicon-check"></span>'
    return sign

def background(is_checked, color):
    if is_checked:
        return ' style="background-color: ' + color + '"'
    return ''

def selected(is_evaluated):
    if is_evaluated:
        return ' class="selected"'
    return ''

@register.simple_tag
def evaluation_options(evaluations, meeting_item, factor, measure_values):

    is_evaluated = False
    reasoning = ''
    for evaluation in evaluations:
        if meeting_item.pk == evaluation.meeting_item.pk \
                and factor.pk == evaluation.factor.pk \
                and evaluation.measure.pk == evaluation.factor.measure.pk:
            is_evaluated = True
            if evaluation.reasoning:
                reasoning = evaluation.reasoning

    html = '''<tr{0}
 data-factor-id="{1}"
 data-measure-id="{2}">
<td>{3}<a href="javascript:void(0);" 
 class="btn-reasoning js-reasoning no-comment pull-right" 
 data-toggle="popover" 
 data-placement="right" 
 data-content="" 
 data-reasoning="{4}">
<span class="fa fa-comment"></span>
</a></td>'''.format(
        selected(is_evaluated),
        factor.pk, 
        factor.measure.pk, 
        factor.name,
        reasoning)

    for measure_value in measure_values:
        is_checked = False
        for evaluation in evaluations:
            if evaluation.measure_value:
                if evaluation.meeting.pk == meeting_item.meeting.pk \
                        and evaluation.meeting_item.pk == meeting_item.pk \
                        and evaluation.factor.pk == factor.pk \
                        and evaluation.measure.pk == factor.measure.pk \
                        and evaluation.measure_value.pk == measure_value.pk:
                    is_checked = True
        html += '''<td class="text-center evaluable" data-color="{0}" data-measure-value-id="{1}"{2}>{3}</td>'''.format(
                measure_value.color, 
                measure_value.pk, 
                background(is_checked, measure_value.color), 
                checksign(is_checked))

    html += '</tr>'

    return html
