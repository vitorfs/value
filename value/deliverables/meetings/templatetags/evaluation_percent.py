from django import template

register = template.Library()

@register.simple_tag
def evaluation_percent(evaluations, meeting_item, factors, measure_value):
    count = 0
    for evaluation in evaluations:
        if evaluation.meeting_item.pk == meeting_item.pk and evaluation.measure.pk == evaluation.factor.measure.pk and evaluation.measure_value.pk == measure_value.pk:
            count = count + 1

    f = len(factors)
    if f > 0:
        percent = int(round(count / float(f), 2) * 100.0)
        return percent
    return '0'
