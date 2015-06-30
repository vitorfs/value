# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliverables', '0009_auto_20150608_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='decisionitemlookup',
            name='column_display',
            field=models.BooleanField(default=True),
        ),
    ]
