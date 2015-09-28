# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0022_ranking_meeting'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ranking',
            unique_together=set([('content_type', 'object_id', 'measure_value')]),
        ),
        migrations.RemoveField(
            model_name='ranking',
            name='meeting_item',
        ),
    ]
