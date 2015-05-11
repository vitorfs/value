from django.db import models
from django.db.models import F
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
    instance = models.ForeignKey(Instance)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2000, null=True, blank=True)
    final_decision = models.NullBooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='deliverable_item_creation_user')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, null=True, related_name='deliverable_item_update_user')
    column_1 = models.CharField(max_length=255, null=True, blank=True)
    column_2 = models.CharField(max_length=255, null=True, blank=True)
    column_3 = models.CharField(max_length=255, null=True, blank=True)
    column_4 = models.CharField(max_length=255, null=True, blank=True)
    column_5 = models.CharField(max_length=255, null=True, blank=True)
    column_6 = models.CharField(max_length=255, null=True, blank=True)
    column_7 = models.CharField(max_length=255, null=True, blank=True)
    column_8 = models.CharField(max_length=255, null=True, blank=True)
    column_9 = models.CharField(max_length=255, null=True, blank=True)
    column_10 = models.CharField(max_length=255, null=True, blank=True)
    column_11 = models.CharField(max_length=255, null=True, blank=True)
    column_12 = models.CharField(max_length=255, null=True, blank=True)
    column_13 = models.CharField(max_length=255, null=True, blank=True)
    column_14 = models.CharField(max_length=255, null=True, blank=True)
    column_15 = models.CharField(max_length=255, null=True, blank=True)
    column_16 = models.CharField(max_length=255, null=True, blank=True)
    column_17 = models.CharField(max_length=255, null=True, blank=True)
    column_18 = models.CharField(max_length=255, null=True, blank=True)
    column_19 = models.CharField(max_length=255, null=True, blank=True)
    column_20 = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Meeting(models.Model):
    name = models.CharField(max_length=255)
    deliverable = models.ForeignKey(Instance)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='meeting_creation_user')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, null=True, related_name='meeting_update_user')    
    
    def __unicode__(self):
        return self.name


class MeetingItems(models.Model):
    meeting = models.ForeignKey(Meeting)
    decision_item = models.ForeignKey(InstanceItem)
    meeting_decision = models.NullBooleanField(null=True, blank=True)

    def __unicode__(self):
        return '{0} {1}'.format(meeting.name, decision_item.name)


class InstanceItemEvaluation(models.Model):
    instance = models.ForeignKey(Instance)
    item = models.ForeignKey(InstanceItem)
    user = models.ForeignKey(User)
    factor = models.ForeignKey(Factor)
    measure = models.ForeignKey(Measure)
    measure_value = models.ForeignKey(MeasureValue, null=True, blank=True)
    evaluated_at = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        mv = 'N/A'
        if self.measure_value:
            mv = self.measure_value.description
        return '{0} {1} {2} {3} {4} {5}'.format(self.instance.name, self.item.name, self.user.username, self.factor.name, self.measure.name, mv)

    @staticmethod
    def get_evaluations_by_instance(instance):
        qs = InstanceItemEvaluation.objects.filter(
            instance=instance, 
            factor__is_active=True, 
            measure__is_active=True).exclude(
            factor__measure=None).filter(
            factor__measure_id=F('measure_id'))
        return qs

    @staticmethod
    def get_user_evaluations_by_instance(user, instance):
        qs = InstanceItemEvaluation.get_evaluations_by_instance(instance).filter(user=user)
        return qs

