from django.db import models
from django.contrib.auth.models import User


class Deliverable(models.Model):
    ONGOING = u'O'
    FINISHED = u'F'
    STATUS = (
        (ONGOING, u'Ongoing'),
        (FINISHED, u'Finished'),
        )

    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2000, null=True, blank=True)
    stakeholders = models.ManyToManyField(User)
    manager = models.ForeignKey(User, related_name='deliverable_manager_user')
    status = models.CharField(max_length=1, choices=STATUS, default=ONGOING)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='deliverable_creation_user')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, null=True, related_name='deliverable_update_user')

    def __unicode__(self):
        return self.name


class DecisionItem(models.Model):
    deliverable = models.ForeignKey(Deliverable)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2000, null=True, blank=True)
    final_decision = models.NullBooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='decision_item_creation_user')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, null=True, related_name='decision_item_update_user')
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
    column_21 = models.CharField(max_length=255, null=True, blank=True)
    column_22 = models.CharField(max_length=255, null=True, blank=True)
    column_23 = models.CharField(max_length=255, null=True, blank=True)
    column_24 = models.CharField(max_length=255, null=True, blank=True)
    column_25 = models.CharField(max_length=255, null=True, blank=True)
    column_26 = models.CharField(max_length=255, null=True, blank=True)
    column_27 = models.CharField(max_length=255, null=True, blank=True)
    column_28 = models.CharField(max_length=255, null=True, blank=True)
    column_29 = models.CharField(max_length=255, null=True, blank=True)
    column_30 = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name

class DecisionItemLookup(models.Model):
    STRING = u'S'
    FLOAT = u'F'
    INTEGER = u'I'
    DATE = u'D'
    DATE_TIME = u'T'
    COLUMN_TYPES = (
        (STRING, u'String'),
        (FLOAT, u'Float'),
        (INTEGER, u'Integer'),
        (DATE, u'Date'),
        (DATE_TIME, u'Date Time'),
        )
    column_name = models.CharField(max_length=255, null=True, blank=True, unique=True)
    column_label = models.CharField(max_length=255, null=True, blank=True)
    column_type = models.CharField(max_length=1, choices=COLUMN_TYPES, default=STRING)
