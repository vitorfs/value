# coding: utf-8

from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from django.db.models import Count, Sum
from django.db.models.signals import m2m_changed
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from value.factors.models import Factor
from value.measures.models import Measure, MeasureValue
from value.deliverables.models import Deliverable, DecisionItem, DecisionItemLookup
from value.deliverables.meetings.utils import format_percentage, get_votes_percentage


class Rationale(models.Model):
    text = models.TextField(_('text'), max_length=4000, null=True, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    created_by = models.ForeignKey(
        User,
        verbose_name=_('created by'),
        on_delete=models.PROTECT,
        related_name='rationales_created'
    )
    updated_by = models.ForeignKey(
        User,
        verbose_name=_('updated by'),
        on_delete=models.PROTECT,
        null=True,
        related_name='rationales_updated'
    )

    class Meta:
        db_table = 'rationales'
        verbose_name = _('rationale')
        verbose_name_plural = _('rationales')

    def __unicode__(self):
        return self.text


class Meeting(models.Model):
    """
    Wraps all the information about a given meeting. The value-based decision-making process
    used in the tool occur per meeting. A meeting is associated with a deliverable, which
    can have many meeting. A meeting has a collection of stakeholders and a collection of
    decision items, defined by the classes MeetingItem and MeetingStakeholder.
    """
    ONGOING = 'O'
    ANALYSING = 'A'
    CLOSED = 'C'
    STATUS = (
        (ONGOING, _('Ongoing')),
        (ANALYSING, _('Analysing')),
        (CLOSED, _('Closed')),
    )

    name = models.CharField('name', max_length=255)
    description = models.CharField('description', max_length=2000, null=True, blank=True)
    location = models.CharField('location', max_length=50, null=True, blank=True)
    deliverable = models.ForeignKey(Deliverable, on_delete=models.PROTECT)
    measure = models.ForeignKey(Measure, on_delete=models.PROTECT, related_name='meetings', null=True)
    factors = models.ManyToManyField(Factor, related_name='meetings')
    status = models.CharField('status', max_length=1, choices=STATUS, default=ONGOING)
    started_at = models.DateTimeField('started at')
    ended_at = models.DateTimeField('ended at', null=True, blank=True)
    created_at = models.DateTimeField('created at', auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        verbose_name='created by',
        on_delete=models.PROTECT,
        related_name='meetings_created'
    )
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    updated_by = models.ForeignKey(
        User,
        verbose_name=_('updated by'),
        on_delete=models.PROTECT,
        null=True,
        related_name='meetings_updated'
    )
    rationales = models.ManyToManyField(Rationale)
    rationales_count = models.PositiveIntegerField(_('rationales count'), default=0)
    progress = models.FloatField(_('progress'), default=0.0)

    class Meta:
        db_table = 'meetings'
        verbose_name = _('meeting')
        verbose_name_plural = _('meetings')
        ordering = ('-updated_at',)

    def __unicode__(self):
        return self.name

    def is_ongoing(self):
        return self.status == Meeting.ONGOING

    def is_analysing(self):
        return self.status == Meeting.ANALYSING

    def is_closed(self):
        return self.status == Meeting.CLOSED

    def get_status_icon_html(self):
        if self.status == Meeting.ONGOING:
            return u'<span class="fa fa-refresh"></span> {0}'.format(self.get_status_display())
        elif self.status == Meeting.ANALYSING:
            return u'<span class="fa fa-bar-chart-o"></span> {0}'.format(self.get_status_display())
        elif self.status == Meeting.CLOSED:
            return u'<span class="fa fa-lock"></span> {0}'.format(self.get_status_display())
        else:
            return self.get_status_display().upper()

    def get_status_label_html(self):
        label = 'label-default'
        if self.status == Meeting.ONGOING:
            label = 'label-success'
        elif self.status == Meeting.ANALYSING:
            label = 'label-warning'
        elif self.status == Meeting.CLOSED:
            label = 'label-danger'
        return u'<span class="label {0}"><span style="text-transform: uppercase;">{1}</span></span>'.format(
            label,
            self.get_status_icon_html()
        )

    def get_evaluations(self):
        return Evaluation.get_evaluations_by_meeting(self)

    def calculate_progress(self):
        """
        Returns the relative progress of a meeting, based on the count of the meeting's stakeholders,
        decision items and the deliverable's factors.
        The maximum number of possible evaluations is the product of multiplying
        TotalEvaluations = MeetingStakeholders * MeetingItems * DeliverableFactors
        The total value is divided by the current number of evaluations, which can't be greater
        then TotalEvaluations.
        """
        stakeholders_count = self.meetingstakeholder_set.count()
        meeting_items_count = self.meetingitem_set.count()
        factors_count = self.factors.count()

        max_evaluations = stakeholders_count * meeting_items_count * factors_count
        total_evaluations = self.get_evaluations().count()

        if max_evaluations != 0:
            percentage = round((total_evaluations / float(max_evaluations)) * 100.0, 2)
        else:
            percentage = 0.0

        self.progress = percentage
        self.save()
        return self.progress

    def calculate_all_rankings(self):
        with transaction.atomic():
            self.ranking_set.all().delete()
            for item in self.meetingitem_set.all():
                item.calculate_ranking()
            for scenario in self.scenarios.all():
                scenario.calculate_ranking()

    def get_stakeholder_groups(self):
        groups = Group.objects.values_list('name', flat=True).order_by('name')

        grouped_stakeholders = {'No group': list()}
        for group in groups:
            grouped_stakeholders[group] = list()

        for meeting_stakeholder in self.meetingstakeholder_set \
                .select_related('stakeholder', 'stakeholder__profile') \
                .all() \
                .order_by('stakeholder__first_name'):
            groups = meeting_stakeholder.stakeholder.groups.all()
            if not groups.exists():
                grouped_stakeholders['No group'].append(meeting_stakeholder.stakeholder)
            else:
                for group in groups:
                    grouped_stakeholders[group.name].append(meeting_stakeholder.stakeholder)
        for name, stakeholders in grouped_stakeholders.items():
            if not any(stakeholders):
                del grouped_stakeholders[name]
        return grouped_stakeholders

    def _get_ordered(self, _class, objects, order, db_model_order):
        """
        Private method to order by database field or evaluation
        ranking. This method should not be used outside this model
        class.
        Used by: get_ordered_meeting_items, get_ordered_scenarios
        """
        can_order_in_db = order in db_model_order
        if can_order_in_db:
            objects = objects.order_by(order)
        else:
            content_type = ContentType.objects.get_for_model(_class)
            ordered_by_ranking = Ranking.objects \
                .filter(content_type=content_type, meeting=self, measure_value__id=order) \
                .order_by('-percentage_votes')
            objects = map(lambda o: o.content_object, ordered_by_ranking)
        return objects

    def get_ordered_meeting_items(self, order):
        """
        Order can represent regular meeting item fields and it's foreign keys.
        It's also possible to pass a MeasureValue id as parameter to order
        by the meeting item ranking.
        """
        meeting_items = self.meetingitem_set.all()
        db_model_order = map(
            lambda key: u'decision_item__{0}'.format(key),
            DecisionItemLookup.get_visible_fields().keys()
        )
        db_model_order.append('-value_ranking')
        return self._get_ordered(MeetingItem, meeting_items, order, db_model_order)

    def get_ordered_scenarios(self, order):
        """
        Order can represent regular scenario fields and it's foreign keys.
        It's also possible to pass a MeasureValue id as parameter to order
        by the scenario ranking.
        """
        scenarios = self.scenarios.all()
        db_model_order = ['-value_ranking', 'name']
        return self._get_ordered(Scenario, scenarios, order, db_model_order)

    def get_meeting_items_rationales_count(self):
        count = 0
        for meeting_item in self.meetingitem_set.all():
            count += meeting_item.get_all_rationales().count()
        return count

    def get_scenarios_rationales_count(self):
        count = 0
        for scenario in self.scenarios.all():
            count += scenario.rationales.count()
        return count

    def calculate_meeting_related_rationales_count(self):
        count = 0
        count += self.get_meeting_items_rationales_count()
        count += self.get_scenarios_rationales_count()
        count += self.rationales.count()
        self.rationales_count = count
        self.save()
        return count

    def initial_data(self, measure_value):
        for stakeholder in self.meetingstakeholder_set.all():
            for meeting_item in self.meetingitem_set.all():
                for factor in self.factors.all():
                    Evaluation.objects.create(
                        meeting=self,
                        meeting_item=meeting_item,
                        user=stakeholder.stakeholder,
                        factor=factor,
                        measure=measure_value.measure,
                        measure_value=measure_value,
                        evaluated_at=timezone.now()
                    )
                meeting_item.calculate_ranking()


class Ranking(models.Model):
    """
    The ranking class is a convenience class, and also to reduce the detabase overhead.
    All the data stored by the Ranking class is calculated based on the Evaluation data.
    Saves for each MeetingItem, separeted by MeasureValue, the total number of votes and
    also the calculated percentage.
    """
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    measure_value = models.ForeignKey(MeasureValue, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    raw_votes = models.IntegerField(_('raw votes'), default=0)
    percentage_votes = models.FloatField(_('percentage votes'), default=0.0)

    class Meta:
        db_table = 'rankings'
        unique_together = (('content_type', 'object_id', 'measure_value',),)
        ordering = ('measure_value__order',)

    def __unicode__(self):
        return '{0}: {1}%'.format(self.measure_value.description, self.percentage_votes)

    def get_percentage_votes_display(self):
        return round(self.percentage_votes, 2)


class MeetingItem(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    decision_item = models.ForeignKey(DecisionItem, on_delete=models.PROTECT)
    meeting_decision = models.BooleanField(_('meeting decision'), default=False)
    rationales = models.ManyToManyField(Rationale)
    has_rationales = models.BooleanField(_('has rationales?'), default=False)
    value_ranking = models.FloatField(_('value ranking'), default=0.0)
    meeting_ranking = models.FloatField(_('meeting ranking'), default=0.0)
    evaluation_summary = GenericRelation(Ranking)

    class Meta:
        db_table = 'meeting_items'
        ordering = ('decision_item__name',)
        verbose_name = _('meeting item')
        verbose_name_plural = _('meeting items')

    def __unicode__(self):
        return u'{0} ({1})'.format(self.decision_item.name, self.meeting.name)

    def get_value_ranking_display(self):
        return format_percentage(self.value_ranking)

    def value_ranking_as_html(self):
        formatted_ranking = self.get_value_ranking_display()
        if self.value_ranking < 0:
            return u'<strong class="text-danger">{0}</strong>'.format(formatted_ranking)
        elif self.value_ranking == 0:
            return u'<strong class="text-warning">{0}</strong>'.format(formatted_ranking)
        else:
            return u'<strong class="text-success">{0}</strong>'.format(formatted_ranking)

    def calculate_ranking(self):
        item_evaluations = Evaluation.get_evaluations_by_meeting(self.meeting) \
            .filter(meeting_item=self)

        measure = self.meeting.measure
        stakeholders_count = self.meeting.meetingstakeholder_set.count()
        factors_count = self.meeting.factors.count()
        max_evaluations = stakeholders_count * factors_count

        rankings = item_evaluations.values('measure_value__id').annotate(votes=Count('measure_value'))

        with transaction.atomic():
            self.evaluation_summary.all().delete()

            meeting_item_content_type = ContentType.objects.get_for_model(MeetingItem)

            for measure_value in measure.measurevalue_set.all():
                Ranking.objects.get_or_create(
                    meeting=self.meeting,
                    content_type=meeting_item_content_type,
                    object_id=self.pk,
                    measure_value=measure_value
                )

            for ranking in rankings:
                votes = int(ranking['votes'])
                percentage = get_votes_percentage(max_evaluations, votes, round_value=False)
                Ranking.objects.filter(
                    meeting=self.meeting,
                    content_type=meeting_item_content_type,
                    object_id=self.pk,
                    measure_value__id=ranking['measure_value__id']
                ).update(raw_votes=votes, percentage_votes=percentage)

            rankings = Ranking.objects.filter(
                meeting=self.meeting,
                content_type=meeting_item_content_type,
                object_id=self.pk
            ).order_by('measure_value__order')

            highest = rankings.first()
            lowest = rankings.last()
            self.value_ranking = highest.percentage_votes - lowest.percentage_votes
            self.save()

    def get_evaluations_with_rationale(self):
        return self.meeting.evaluation_set \
            .filter(meeting_item=self) \
            .exclude(rationale=None) \
            .order_by('factor__name')

    def update_has_rationales(self):
        has_evaluation_rationales = self.get_evaluations_with_rationale().exists()
        has_meeting_item_rationales = self.rationales.exists()
        self.has_rationales = has_evaluation_rationales or has_meeting_item_rationales
        self.save()
        return self.has_rationales

    def get_all_rationales(self):
        evaluations = self.get_evaluations_with_rationale()
        evaluation_rationales = Rationale.objects.filter(evaluation__in=evaluations)
        return evaluation_rationales | self.rationales.all()


class MeetingStakeholder(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    stakeholder = models.ForeignKey(User, on_delete=models.PROTECT)
    meeting_input = models.FloatField(_('meeting input'), default=0.0)

    class Meta:
        db_table = 'meeting_stakeholders'
        ordering = ('stakeholder__first_name', 'stakeholder__last_name', 'stakeholder__username')

    def __unicode__(self):
        return '{0} - {1}'.format(self.meeting.name, self.stakeholder.username)


class Evaluation(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.PROTECT)
    meeting_item = models.ForeignKey(MeetingItem, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    factor = models.ForeignKey(Factor, on_delete=models.PROTECT)
    measure = models.ForeignKey(Measure, on_delete=models.PROTECT)
    measure_value = models.ForeignKey(MeasureValue, on_delete=models.SET_NULL, null=True, blank=True)
    evaluated_at = models.DateTimeField(_('evaluated at'), null=True, blank=True)
    rationale = models.OneToOneField(Rationale, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'evaluations'
        unique_together = (('meeting', 'meeting_item', 'user', 'factor', 'measure'), )
        verbose_name = _('evaluation')
        verbose_name_plural = _('evaluations')

    def __unicode__(self):
        return '{0} - {1}'.format(self.meeting.name, self.meeting_item.decision_item.name)

    @staticmethod
    def _list(meeting):
        return Evaluation.objects.filter(
            meeting=meeting,
            factor__in=meeting.factors.all(),
            measure=meeting.measure
        )

    @staticmethod
    def get_evaluations_by_meeting(meeting):
        return Evaluation._list(meeting).exclude(measure_value=None)

    @staticmethod
    def get_user_evaluations_by_meeting(user, meeting):
        return Evaluation._list(meeting).filter(user=user)


class Scenario(models.Model):
    """
    The Scenario class is used to aggregate decision items to generate different
    types of visualization inside the dashboard.
    """
    name = models.CharField(_('name'), max_length=255)
    meeting = models.ForeignKey(Meeting, on_delete=models.PROTECT, related_name='scenarios')
    meeting_items = models.ManyToManyField(MeetingItem, related_name='scenarios')
    value_ranking = models.FloatField(_('value ranking'), default=0.0)
    evaluation_summary = GenericRelation(Ranking)
    rationales = models.ManyToManyField(Rationale)

    class Meta:
        db_table = 'scenarios'
        unique_together = (('name', 'meeting',),)

    def __unicode__(self):
        return self.name

    def _generate_unique_name(self, base_name):
        name = base_name
        name_count = 1
        while Scenario.objects.filter(meeting=self.meeting, name=name).exists():
            name_count += 1
            name = u'{0} ({1})'.format(base_name, name_count)
        return name

    def build(self, *args, **kwargs):
        limit = int(kwargs.get('meeting_items_count'))
        measure_value = kwargs.get('criteria')
        name = kwargs.get('name')
        factors = kwargs.get('factors')

        evaluations = self.meeting.get_evaluations()
        scenario_items = evaluations.filter(measure_value=measure_value, factor__in=factors) \
            .values_list('meeting_item', flat=True) \
            .annotate(count=Count('measure_value')) \
            .order_by('-count')[:limit]

        with transaction.atomic():
            self.name = self._generate_unique_name(name)
            self.save()
            self.meeting_items.add(*scenario_items)

        return self

    def get_value_ranking_display(self):
        return format_percentage(self.value_ranking)

    def calculate_ranking(self):
        meeting_items_count = self.meeting_items.count()
        stakeholders_count = self.meeting.meetingstakeholder_set.count()
        factors_count = self.meeting.factors.count()
        max_evaluations = stakeholders_count * factors_count * meeting_items_count

        with transaction.atomic():
            value_ranking_sum = self.meeting_items.aggregate(total=Sum('value_ranking'))
            meeting_items_ranking = value_ranking_sum['total']
            if meeting_items_count > 0:
                self.value_ranking = meeting_items_ranking / float(meeting_items_count)
            else:
                self.value_ranking = 0.0
            self.save()

            self.evaluation_summary.all().delete()
            aggregated_measure_values = dict()

            # Initialize the aggregated_measure_values dict to make sure
            # it's gonna have all possible Measure Value, even if no meeting item
            # has received a vote for that Measure Value.
            for measure_value in self.meeting.measure.measurevalue_set.all():
                aggregated_measure_values[measure_value.pk] = 0

            for meeting_item in self.meeting_items.all():
                for ranking in meeting_item.evaluation_summary.all():
                    if ranking.measure_value.pk not in aggregated_measure_values.keys():
                        aggregated_measure_values[measure_value.pk] = 0
                    aggregated_measure_values[ranking.measure_value.pk] += ranking.raw_votes

            for measure_value_id, raw_votes in aggregated_measure_values.iteritems():
                percentage_votes = get_votes_percentage(max_evaluations, raw_votes, round_value=False)
                measure_value = MeasureValue.objects.get(pk=measure_value_id)
                Ranking.objects.create(
                    content_object=self,
                    meeting=self.meeting,
                    measure_value=measure_value,
                    raw_votes=raw_votes,
                    percentage_votes=percentage_votes
                )


def calculate_scenario_ranking(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove']:
        instance.calculate_ranking()

m2m_changed.connect(calculate_scenario_ranking, sender=Scenario.meeting_items.through)


def calculate_rationales_count(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove']:
        if isinstance(instance, Meeting):
            meeting = instance
        else:
            meeting = instance.meeting
        meeting.calculate_meeting_related_rationales_count()

m2m_changed.connect(calculate_rationales_count, sender=Meeting.rationales.through)
m2m_changed.connect(calculate_rationales_count, sender=MeetingItem.rationales.through)
m2m_changed.connect(calculate_rationales_count, sender=Scenario.rationales.through)
