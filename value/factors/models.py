# coding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _

from value.measures.models import Measure


class Group(models.Model):
    name = models.CharField(_('name'), max_length=255, unique=True)

    class Meta:
        db_table = 'factors_groups'
        verbose_name = _('value factors group')
        verbose_name_plural = _('value factors groups')

    def __unicode__(self):
        return self.name


class Factor(models.Model):
    name = models.CharField(_('name'), max_length=255, unique=True)
    description = models.TextField(_('description'), max_length=2000, null=True, blank=True)
    measure = models.ForeignKey(Measure, null=True, blank=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(_('active'), default=True)
    group = models.ForeignKey(Group, null=True, blank=True, verbose_name=_('group'), on_delete=models.SET_NULL)

    class Meta:
        db_table = 'factors'
        ordering = ('group', 'name',)
        verbose_name = _('value factor')
        verbose_name_plural = _('value factors')

    def __unicode__(self):
        return self.name
