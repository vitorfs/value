from django.db import models
from django.db.models import F
from django.contrib.auth.models import User

from value.factors.models import Factor
from value.measures.models import Measure, MeasureValue
from value.deliverables.models import Deliverable, DecisionItem

class Meeting(models.Model):
    name = models.CharField(max_length=255)
    deliverable = models.ForeignKey(Deliverable)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='meeting_creation_user')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, null=True, related_name='meeting_update_user')    
    
    def __unicode__(self):
        return self.name

    def get_evaluations(self):
        return Evaluation.get_evaluations_by_meeting(self)

    def get_progress(self):
        stakeholders_count = self.meetingstakeholder_set.count()
        meeting_items_count = self.meetingitem_set.count()
        factors_count = Factor.get_factors().count()

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

    def __unicode__(self):
        return '{0} {1}'.format(self.meeting.name, self.decision_item.name)


class MeetingStakeholder(models.Model):
    meeting = models.ForeignKey(Meeting)
    stakeholder = models.ForeignKey(User)
    meeting_input = models.FloatField(default=0.0)

    class Meta:
        ordering = ('stakeholder__first_name', 'stakeholder__last_name', 'stakeholder__username',)

    def __unicode__(self):
        return '{0} {1}'.format(self.meeting.name, self.stakeholder.username)


class Evaluation(models.Model):
    meeting = models.ForeignKey(Meeting)
    meeting_item = models.ForeignKey(MeetingItem)
    user = models.ForeignKey(User)
    factor = models.ForeignKey(Factor)
    measure = models.ForeignKey(Measure)
    measure_value = models.ForeignKey(MeasureValue, null=True, blank=True)
    evaluated_at = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        mv = 'N/A'
        if self.measure_value:
            mv = self.measure_value.description
        return '{0} {1} {2} {3} {4} {5}'.format(self.meeting.name, self.meeting_item.decision_item.name, self.user.username, self.factor.name, self.measure.name, mv)

    @staticmethod
    def get_evaluations_by_meeting(meeting):
        qs = Evaluation.objects.filter(
            meeting=meeting, 
            factor__is_active=True, 
            measure__is_active=True).exclude(
            factor__measure=None).filter(
            factor__measure_id=F('measure_id'))
        return qs

    @staticmethod
    def get_user_evaluations_by_meeting(user, meeting):
        qs = Evaluation.get_evaluations_by_meeting(meeting).filter(user=user)
        return qs
