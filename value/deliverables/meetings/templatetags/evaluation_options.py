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
def evaluation_options(evaluations, meeting_item, factor):

    is_evaluated = False
    for evaluation in evaluations:
        if meeting_item.pk == evaluation.meeting_item.pk and factor.pk == evaluation.factor.pk and evaluation.measure.pk == evaluation.factor.measure.pk:
            is_evaluated = True

    html = '<tr{0}><td>{1}</td>'.format(selected(is_evaluated), factor.name)

    for measure_value in factor.measure.measurevalue_set.all():
        is_checked = False
        for evaluation in evaluations:
            if evaluation.measure_value:
                if evaluation.meeting.pk == meeting_item.meeting.pk and evaluation.meeting_item.pk == meeting_item.pk and evaluation.factor.pk == factor.pk and evaluation.measure.pk == factor.measure.pk and evaluation.measure_value.pk == measure_value.pk:
                    is_checked = True
        html += '''<td class="text-center evaluable" 
data-color="{0}" 
data-deliverable-id="{1}"
data-meeting-id="{2}" 
data-meeting-item-id="{3}"
data-factor-id="{4}" 
data-measure-id="{5}" 
data-measure-value-id="{6}"
{7}>
{8}
</td>'''.format(
    measure_value.color, 
    meeting_item.meeting.deliverable.pk,
    meeting_item.meeting.pk, 
    meeting_item.pk, 
    factor.pk, 
    factor.measure.pk, 
    measure_value.pk, 
    background(is_checked, measure_value.color), 
    checksign(is_checked)
    )

    html += '</tr>'

    return html
