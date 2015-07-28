# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0003_auto_20150714_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factor',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='factors.Group', null=True),
        ),
    ]
