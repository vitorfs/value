from django import template

register = template.Library()

@register.simple_tag
def panel_class(evaluations, meeting_item, factors):
    return 'panel-default'
    count = 0
    for evaluation in evaluations.exclude(measure_value=None):
        if evaluation.meeting_item == meeting_item and evaluation.measure == evaluation.factor.measure:
            count = count + 1

    if count == len(factors):
        return 'panel-success'
    return 'panel-default'
