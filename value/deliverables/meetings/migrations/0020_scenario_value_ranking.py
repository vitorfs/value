# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0019_auto_20150923_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenario',
            name='value_ranking',
            field=models.FloatField(default=0.0),
        ),
    ]
