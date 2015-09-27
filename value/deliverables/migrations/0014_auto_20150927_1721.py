# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliverables', '0013_auto_20150909_1219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='decisionitem',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='decisionitem',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='decisionitem',
            name='final_decision',
        ),
        migrations.RemoveField(
            model_name='decisionitem',
            name='ranking',
        ),
        migrations.RemoveField(
            model_name='decisionitem',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='decisionitem',
            name='updated_by',
        ),
    ]
