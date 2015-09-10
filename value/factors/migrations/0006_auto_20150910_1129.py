# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0005_auto_20150729_1555'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factor',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='factor',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='factor',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='factor',
            name='updated_by',
        ),
    ]
