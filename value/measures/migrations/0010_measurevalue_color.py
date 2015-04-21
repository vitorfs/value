# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measures', '0009_auto_20150421_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurevalue',
            name='color',
            field=models.CharField(max_length=6, null=True, blank=True),
        ),
    ]
