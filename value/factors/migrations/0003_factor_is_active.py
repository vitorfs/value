# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0002_auto_20150413_0854'),
    ]

    operations = [
        migrations.AddField(
            model_name='factor',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
