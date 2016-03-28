# coding: utf-8

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_scenarios_selection(value):
    if len(value) != 2:
        raise ValidationError(_('Select exactly two scenarios to compare.'))
