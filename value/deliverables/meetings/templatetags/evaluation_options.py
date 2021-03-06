# coding: utf-8

from django import template
from django.utils.html import escape, mark_safe
from django.utils.translation import ugettext as _

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
def evaluation_options(evaluations, meeting_item, factor, measure, measure_values):
    if meeting_item.meeting.is_closed():
        can_evaluate = 'not-evaluable'
    else:
        can_evaluate = 'evaluable'

    is_evaluated = False
    rationale_text = ''
    no_comment = 'no-comment'
    for evaluation in evaluations:
        if meeting_item == evaluation.meeting_item \
                and measure == evaluation.measure \
                and factor == evaluation.factor:
            if evaluation.measure_value is not None:
                is_evaluated = True
            if evaluation.rationale and evaluation.rationale.text != '':
                rationale_text = evaluation.rationale.text
                no_comment = ''

    html = '<tr{0} data-factor-id="{1}" data-measure-id="{2}">'.format(
        selected(is_evaluated),
        factor.pk,
        measure.pk
    )

    factor_name = factor.name
    if factor.group:
        factor_name = u'{0}: <strong>{1}</strong>'.format(escape(factor.group.name), escape(factor.name))

    factor_description = _('No description')
    if factor.description:
        factor_description = escape(factor.description)

    html += u'''<td>
 <span class="js-factor-description help-cursor"
       data-content="{3}"
       data-container="#factor-description-container"
       data-trigger="hover">{0}</span>
 <a href="javascript:void(0);"
 class="btn-rationale js-rationale {1} pull-right"
 data-toggle="popover"
 data-placement="right"
 title="{4} {0}"
 data-content=""
 data-rationale="{2}">
<span class="fa fa-comment"></span>
</a></td>'''.format(
        factor_name,
        no_comment,
        escape(rationale_text),
        factor_description,
        _('Add a rationale for')
    )

    for measure_value in measure_values:
        is_checked = False
        for evaluation in evaluations:
            if evaluation.measure_value:
                if evaluation.meeting.pk == meeting_item.meeting.pk \
                        and evaluation.meeting_item.pk == meeting_item.pk \
                        and evaluation.factor.pk == factor.pk \
                        and evaluation.measure == measure \
                        and evaluation.measure_value.pk == measure_value.pk:
                    is_checked = True
        html += '''<td class="text-center {0}" data-color="{1}" data-measure-value-id="{2}"{3}>{4}</td>'''.format(
            can_evaluate,
            measure_value.color,
            measure_value.pk,
            background(is_checked, measure_value.color),
            checksign(is_checked)
        )
    html += '</tr>'
    return mark_safe(html)
