from django import template

register = template.Library()

@register.simple_tag
def panel_class(evaluations, item, factors):
    count = 0
    for evaluation in evaluations:
        if evaluation.item.pk == item.pk and evaluation.measure.pk == evaluation.factor.measure.pk:
            count = count + 1

    if count == len(factors):
        return 'panel-success'
    return 'panel-default'
