from django.db import models

class Rating(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    def get_values(self):
        values = RatingValue.objects.filter(rating=self)
        string_values = []
        for value in values:
            string_values.append(value.description)
        return u', '.join(string_values)


class RatingValue(models.Model):
    rating = models.ForeignKey(Rating)
    description = models.CharField(max_length=255)
    weight = models.FloatField()

    class Meta:
        ordering = ("-weight",)

    def __unicode__(self):
        return self.description
