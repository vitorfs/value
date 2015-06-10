# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0010_auto_20150609_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetingitem',
            name='value_ranking',
            field=models.FloatField(default=0.0),
        ),
    ]
