# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0006_auto_20150430_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instanceitemevaluation',
            name='evaluated_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='instanceitemevaluation',
            name='measure_value',
            field=models.ForeignKey(blank=True, to='measures.MeasureValue', null=True),
        ),
    ]
