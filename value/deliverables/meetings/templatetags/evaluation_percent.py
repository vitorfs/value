from django import template

register = template.Library()

@register.simple_tag
def evaluation_percent(evaluations, meeting_item, factors, measure, measure_value):
    count = 0
    for evaluation in evaluations:
        if evaluation.meeting_item == meeting_item and \
                evaluation.measure == measure and \
                evaluation.measure_value == measure_value:
            count = count + 1

    f = len(factors)
    if f > 0:
        percent = (count / float(f)) * 100.0
        return percent
    return 0

@register.simple_tag
def evaluation_percent_display(evaluations, meeting_item, factors, measure, measure_value):
    percent = evaluation_percent(evaluations, meeting_item, factors, measure, measure_value)
    return '{0:.2f}'.format(percent)
