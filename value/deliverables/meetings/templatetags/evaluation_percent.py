from django import template

register = template.Library()

@register.simple_tag
def evaluation_percent(evaluations, meeting_item, factors, measure_value):
    count = 0
    for evaluation in evaluations:
        if evaluation.meeting_item == meeting_item and evaluation.measure == evaluation.factor.measure and evaluation.measure_value == measure_value:
            count = count + 1

    f = len(factors)
    if f > 0:
        percent = (count / float(f)) * 100.0
        return '{0:.2f}'.format(percent)
    return '0'
