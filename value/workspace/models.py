from django.db import models
from django.contrib.auth.models import User
from value.factors.models import Factor
from value.measures.models import Measure, MeasureValue

class Instance(models.Model):
    INITIALIZED = u'I'
    RUNNING = u'R'
    FINISHED = u'F'
    STATUS = (
        (INITIALIZED, u'Initialized'),
        (RUNNING, u'Running'),
        (FINISHED, u'Finished'),
        )

    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2000, null=True, blank=True)
    stakeholders = models.ManyToManyField(User)
    manager = models.ForeignKey(User, related_name='instance_manager_user')
    status = models.CharField(max_length=1, choices=STATUS, default=INITIALIZED)
    has_backlog = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='instance_creation_user')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, null=True, related_name='instance_update_user')

    def __unicode__(self):
        return self.name

    def get_items(self):
        return InstanceItem.objects.filter(instance=self)

class InstanceItem(models.Model):
    name = models.CharField(max_length=255)
    instance = models.ForeignKey(Instance)

    def __unicode__(self):
        return self.name

class InstanceItemEvaluation(models.Model):
    instance = models.ForeignKey(Instance)
    user = models.ForeignKey(User)
    factor = models.ForeignKey(Factor)
    measure = models.ForeignKey(Measure)
    measure_value = models.ForeignKey(MeasureValue)
    evaluated_at = models.DateTimeField(auto_now=True)
