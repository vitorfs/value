from django import template

register = template.Library()

@register.simple_tag
def evaluation_percent(evaluations, item, factors):
    count = 0
    for evaluation in evaluations:
        if evaluation.item.pk == item.pk and evaluation.measure.pk == evaluation.factor.measure.pk:
            count = count + 1

    f = len(factors)
    if f > 0:
        percent = int(round(count / float(f), 2) * 100.0)
        return '{0}%'.format(percent)
    return '0%'
