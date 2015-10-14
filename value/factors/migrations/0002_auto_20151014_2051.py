# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factor',
            name='measure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='measures.Measure', null=True),
        ),
    ]
