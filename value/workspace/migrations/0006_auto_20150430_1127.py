# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0005_instanceitemevaluation_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instanceitemevaluation',
            name='evaluated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 30, 8, 27, 21, 168663, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='instanceitemevaluation',
            name='measure_value',
            field=models.ForeignKey(default=1, to='measures.MeasureValue'),
            preserve_default=False,
        ),
    ]
