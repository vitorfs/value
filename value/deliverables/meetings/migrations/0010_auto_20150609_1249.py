# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0009_ranking'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ranking',
            options={'ordering': ('meeting_item__decision_item__description', 'measure_value__order')},
        ),
        migrations.AlterUniqueTogether(
            name='ranking',
            unique_together=set([('meeting_item', 'measure_value')]),
        ),
    ]
