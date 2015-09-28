# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('meetings', '0020_scenario_value_ranking'),
    ]

    operations = [
        migrations.AddField(
            model_name='ranking',
            name='content_type',
            field=models.ForeignKey(default=12, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ranking',
            name='object_id',
            field=models.PositiveIntegerField(default=31),
            preserve_default=False,
        ),
    ]
