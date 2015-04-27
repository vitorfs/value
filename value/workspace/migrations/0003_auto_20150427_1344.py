# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0002_instanceitemevaluation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instanceitemevaluation',
            name='measure_value',
            field=models.ForeignKey(blank=True, to='measures.MeasureValue', null=True),
        ),
    ]
