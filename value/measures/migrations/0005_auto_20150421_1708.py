# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measures', '0004_auto_20150421_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurevalue',
            name='description',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='measurevalue',
            name='order',
            field=models.IntegerField(default=0, blank=True),
        ),
    ]
