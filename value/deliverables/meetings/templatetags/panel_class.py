from django import template

register = template.Library()

@register.simple_tag
def panel_class(evaluations, meeting_item, factors):
    count = 0
    for evaluation in evaluations:
        if evaluation.meeting_item.pk == meeting_item.pk and evaluation.measure.pk == evaluation.factor.measure.pk:
            count = count + 1

    if count == len(factors):
        return 'panel-success'
    return 'panel-default'
