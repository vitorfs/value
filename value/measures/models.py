# coding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Measure(models.Model):
    """
        Measures used in the decision-making process. There should be only one
        active (is_active = True) measure object within the context of the
        application.
    """
    name = models.CharField(_('name'), max_length=255, unique=True)
    is_active = models.BooleanField(_('active'), default=True)

    class Meta:
        db_table = 'measures'
        verbose_name = _('measure')
        verbose_name_plural = _('measures')

    def __unicode__(self):
        return self.name

    def get_values_as_string(self):
        """
            Parse all MeasureValue objects into a string formatted shape with
            small colored squares.
            The output should look like '[#] Positive, [#] Neutral, [#] Negative'.
        """
        string_values = []
        for value in self.measurevalue_set.all():
            string_values.append(
                u'<span class="measure-square" style="background-color: {1};"></span> {0}'.format(
                    value.description,
                    value.color
                )
            )
        return u', '.join(string_values)

    def get_grouped_measure_values(self):
        grouped_measure_values = list()
        measure_values = self.measurevalue_set.order_by('order')
        total_values = measure_values.count()
        half_index = int(round(total_values / 2.0))

        positive_list = list()
        neutral_list = list()
        negative_list = list()

        if total_values % 2 == 0:
            # The measure values are evenly distributed (half good / half bad) or (half positive / half negative)
            for index, measure_value in enumerate(measure_values):
                if (index + 1) <= half_index:
                    positive_list.append(measure_value)
                else:
                    negative_list.append(measure_value)
            grouped_measure_values = [positive_list, negative_list, ]
        else:
            # Means there is a central point, usually (neutral / medium / normal)
            for index, measure_value in enumerate(measure_values):
                if (index + 1) < half_index:
                    positive_list.append(measure_value)
                elif (index + 1) == half_index:
                    neutral_list.append(measure_value)
                else:
                    negative_list.append(measure_value)
            grouped_measure_values = [positive_list, neutral_list, negative_list, ]
        return grouped_measure_values


class MeasureValue(models.Model):

    PRIMARY_BLUE = '#337BB7'

    COLORS = (
        ('#5CB85C', '#5CB85C'),
        ('#BAE8BA', '#BAE8BA'),
        ('#8AD38A', '#8AD38A'),
        ('#369836', '#369836'),
        ('#1B7C1B', '#1B7C1B'),

        ('#F0AD4E', '#F0AD4E'),
        ('#FFD8A0', '#FFD8A0'),
        ('#FFC675', '#FFC675'),
        ('#DE9226', '#DE9226'),
        ('#AD6D11', '#AD6D11'),

        ('#D9534F', '#D9534F'),
        ('#FFADAB', '#FFADAB'),
        ('#FC827F', '#FC827F'),
        ('#BE2F2B', '#BE2F2B'),
        ('#961512', '#961512'),

        ('#5BC1DE', '#5BC1DE'),
        ('#BAEAF8', '#BAEAF8'),
        ('#85D5EC', '#85D5EC'),
        ('#39ACCD', '#39ACCD'),
        ('#1993B6', '#1993B6'),

        (PRIMARY_BLUE, '#337BB7'),
        ('#7EB1DC', '#7EB1DC'),
        ('#5393C8', '#5393C8'),
        ('#1265AB', '#1265AB'),
        ('#094B83', '#094B83'),

        ('#222222', '#222222'),
        ('#929191', '#929191'),
        ('#5E5E5E', '#5E5E5E'),
        ('#000000', '#000000'),
        ('#030202', '#030202'),
    )
    measure = models.ForeignKey(Measure)
    description = models.CharField(_('description'), max_length=255)
    order = models.IntegerField(_('order'), default=0)
    color = models.CharField(_('color'), max_length=7, choices=COLORS, default=PRIMARY_BLUE)

    class Meta:
        db_table = 'measure_values'
        ordering = ('order',)
        verbose_name = _('measure value')
        verbose_name_plural = _('measure values')

    def __unicode__(self):
        return self.description
