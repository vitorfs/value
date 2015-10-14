from django.db import models
from django.contrib.auth.models import User

from value.measures.models import Measure


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'factors_groups'

    def __unicode__(self):
        return self.name

class Factor(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=2000, null=True, blank=True)
    measure = models.ForeignKey(Measure, null=True, blank=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)
    group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'factors'
        ordering = ('group', 'name',)

    def __unicode__(self):
        return self.name
