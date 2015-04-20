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
        string_values = []
        for value in values:
            string_values.append(value.description)
        return u', '.join(string_values)


class MeasureValue(models.Model):
    measure = models.ForeignKey(Measure)
    description = models.CharField(max_length=255)
    weight = models.FloatField()

    class Meta:
        ordering = ("-weight",)

    def __unicode__(self):
        return self.description
