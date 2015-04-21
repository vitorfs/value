from django.db import models
from django.contrib.auth.models import User

class Measure(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='measure_creation_user')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, null=True, related_name='measure_update_user')

    def __unicode__(self):
        return self.name

    def get_values(self):
        values = MeasureValue.objects.filter(measure=self)
        return values

    def get_values_as_string(self):
        values = self.get_values()
        string_values = []
        for value in values:
            string_values.append(value.description)
        return u', '.join(string_values)


class MeasureValue(models.Model):

    LIME_GREEN = u'#32CD32'
    COLORS = (
        (u'#A0522D', u'sienna'),
        (u'#CD5C5C', u'indianred'),
        (u'#FF4500', u'orangered'),
        (u'#008B8B', u'darkcyan'),
        (u'#B8860B', u'darkgoldenrod'),
        (LIME_GREEN, u'limegreen'),
        (u'#FFD700', u'gold'),
        (u'#48D1CC', u'mediumturquoise'),
        (u'#87CEEB', u'skyblue'),
        (u'#FF69B4', u'hotpink'),
        (u'#CD5C5C', u'indianred'),
        (u'#87CEFA', u'lightskyblue'),
        (u'#6495ED', u'cornflowerblue'),
        (u'#DC143C', u'crimson'),
        (u'#FF8C00', u'darkorange'),
        (u'#C71585', u'mediumvioletred'),
        (u'#000000', u'black'),
        )
    measure = models.ForeignKey(Measure)
    description = models.CharField(max_length=255, null=True, blank=True)
    order = models.IntegerField(default=0, null=True, blank=True)
    color = models.CharField(max_length=7, null=True, blank=True, choices=COLORS, default=LIME_GREEN)

    class Meta:
        ordering = ("order",)

    def __unicode__(self):
        return self.description
