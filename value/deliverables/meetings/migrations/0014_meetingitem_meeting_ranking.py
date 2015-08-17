# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0013_auto_20150812_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetingitem',
            name='meeting_ranking',
            field=models.FloatField(default=0.0),
        ),
    ]
