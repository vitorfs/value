from django.db import models
from django.contrib.auth.models import User

from value.core.exceptions import MeasureImproperlyConfigured


class Measure(models.Model):
    """
    Measures used in the decision-making process. There should be only one
    active (is_active = True) measure object within the context of the
    application.
    """
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='measure_creation_user')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, null=True, related_name='measure_update_user')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Override base save method to ensure there is only one active measure
        in the context of the application.
        """
        if self.is_active:
            Measure.objects.all().update(is_active=False)
        super(Measure, self).save(*args, **kwargs)

    @staticmethod
    def get():
        """
        Return the active measure only if it is properly configured.
        Otherwise return a MeasureImproperlyConfigured exception.
        """
        measures = Measure.objects.filter(is_active=True)
        measure = None
        if not measures:
            raise MeasureImproperlyConfigured('There is no active measure in the application.')
        else:
            measure = measures[0]
            if measure.measurevalue_set.count() < 2:
                raise MeasureImproperlyConfigured('The current active measure has less than two measure values.')
        return measure

    def get_values_as_string(self):
        """
        Parse all MeasureValue objects into a string formatted shape.
        The output should look like 'Positive, Neutral, Negative'.
        """
        string_values = []
        for value in self.measurevalue_set.all():
            string_values.append(value.description)
        return u', '.join(string_values)


class MeasureValue(models.Model):

    PRIMARY_BLUE = u'#337BB7'

    COLORS = (
        (u'#5CB85C', u'#5CB85C'),
        (u'#BAE8BA', u'#BAE8BA'),
        (u'#8AD38A', u'#8AD38A'),
        (u'#369836', u'#369836'),
        (u'#1B7C1B', u'#1B7C1B'),

        (u'#F0AD4E', u'#F0AD4E'),
        (u'#FFD8A0', u'#FFD8A0'),
        (u'#FFC675', u'#FFC675'),
        (u'#DE9226', u'#DE9226'),
        (u'#AD6D11', u'#AD6D11'),

        (u'#D9534F', u'#D9534F'),
        (u'#FFADAB', u'#FFADAB'),
        (u'#FC827F', u'#FC827F'),
        (u'#BE2F2B', u'#BE2F2B'),
        (u'#961512', u'#961512'),

        (u'#5BC1DE', u'#5BC1DE'),
        (u'#BAEAF8', u'#BAEAF8'),
        (u'#85D5EC', u'#85D5EC'),
        (u'#39ACCD', u'#39ACCD'),
        (u'#1993B6', u'#1993B6'),

        (PRIMARY_BLUE, u'#337BB7'),
        (u'#7EB1DC', u'#7EB1DC'),
        (u'#5393C8', u'#5393C8'),
        (u'#1265AB', u'#1265AB'),
        (u'#094B83', u'#094B83'),

        (u'#222222', u'#222222'),
        (u'#929191', u'#929191'),
        (u'#5E5E5E', u'#5E5E5E'),
        (u'#000000', u'#000000'),
        (u'#030202', u'#030202'),
        )
    measure = models.ForeignKey(Measure)
    description = models.CharField(max_length=255, null=True, blank=True)
    order = models.IntegerField(default=0, null=True, blank=True)
    color = models.CharField(max_length=7, null=True, blank=True, choices=COLORS, default=PRIMARY_BLUE)

    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return self.description
