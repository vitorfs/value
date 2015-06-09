from django.db import models
from django.db.models import F
from django.contrib.auth.models import User

from value.factors.models import Factor
from value.measures.models import Measure, MeasureValue
from value.deliverables.models import Deliverable, DecisionItem, Rationale


class Meeting(models.Model):
    """
    Wraps all the information about a given meeting. The value-based decison-making process
    used in the tool occur per meeting. A meeting is associated with a deliverable, which
    can have many meeting. A meeting has a collection of stakeholders and a collection of
    decision items, defined by the classes MeetingItem and MeetingStakeholder.
    """
    ONGOING = u'O'
    CLOSED = u'C'
    STATUS = (
        (ONGOING, u'Ongoing'),
        (CLOSED, u'Closed'),
        )

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2000, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    deliverable = models.ForeignKey(Deliverable)
    status = models.CharField(max_length=1, choices=STATUS, default=ONGOING)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='meeting_creation_user')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, null=True, related_name='meeting_update_user')    
    
    class Meta:
        ordering = ('-updated_at',)

    def __unicode__(self):
        return self.name

    def is_closed(self):
        return self.status == Meeting.CLOSED

    def get_status_label_html(self):
        if self.status == self.ONGOING:
            return u'<span class="label {0}">{1}</span>'.format("label-success", self.get_status_display().upper())
        elif self.status == self.CLOSED:
            return u'<span class="label {0}">{1}</span>'.format("label-warning", self.get_status_display().upper())
        else:
            return u'<span class="label {0}">{1}</span>'.format("label-default", self.get_status_display().upper())

    def get_evaluations(self):
        return Evaluation.get_evaluations_by_meeting(self)

    def get_progress(self):
        stakeholders_count = self.meetingstakeholder_set.count()
        meeting_items_count = self.meetingitem_set.count()
        factors_count = Factor.list().count()

        max_evaluations = stakeholders_count * meeting_items_count * factors_count
        total_evaluations = self.get_evaluations().count()

        if max_evaluations != 0:
            percentage = round((total_evaluations / float(max_evaluations)) * 100.0, 2)
        else:
            percentage = 0.0

        return percentage


class MeetingItem(models.Model):
    meeting = models.ForeignKey(Meeting)
    decision_item = models.ForeignKey(DecisionItem)
    meeting_decision = models.NullBooleanField(null=True, blank=True)
    rationales = models.ManyToManyField(Rationale)

    def __unicode__(self):
        return '{0} - {1}'.format(self.meeting.name, self.decision_item.name)


class MeetingStakeholder(models.Model):
    meeting = models.ForeignKey(Meeting)
    stakeholder = models.ForeignKey(User)
    meeting_input = models.FloatField(default=0.0)

    class Meta:
        ordering = ('stakeholder__first_name', 'stakeholder__last_name', 'stakeholder__username',)

    def __unicode__(self):
        return '{0} - {1}'.format(self.meeting.name, self.stakeholder.username)


class Evaluation(models.Model):
    meeting = models.ForeignKey(Meeting)
    meeting_item = models.ForeignKey(MeetingItem)
    user = models.ForeignKey(User)
    factor = models.ForeignKey(Factor)
    measure = models.ForeignKey(Measure)
    measure_value = models.ForeignKey(MeasureValue, null=True, blank=True)
    evaluated_at = models.DateTimeField(null=True, blank=True)
    rationale = models.OneToOneField(Rationale, null=True)

    class Meta:
        unique_together = (('meeting', 'meeting_item', 'user', 'factor', 'measure'),)

    def __unicode__(self):
        return '{0} - {1}'.format(self.meeting.name, self.meeting_item.decision_item.name)

    @staticmethod
    def _list(meeting):
        qs = Evaluation.objects.filter(
            meeting=meeting, 
            factor__is_active=True, 
            measure__is_active=True).exclude(
            factor__measure=None).filter(
            factor__measure_id=F('measure_id'))
        return qs

    @staticmethod
    def get_evaluations_by_meeting(meeting):
        return Evaluation._list(meeting).exclude(measure_value=None)

    @staticmethod
    def get_user_evaluations_by_meeting(user, meeting):
        return Evaluation._list(meeting).filter(user=user)
