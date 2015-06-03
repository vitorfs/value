# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliverables', '0004_auto_20150603_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='decisionitem',
            name='ranking',
            field=models.FloatField(default=0.0),
        ),
    ]
