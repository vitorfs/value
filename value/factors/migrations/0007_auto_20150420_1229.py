# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measures', '0001_initial'),
        ('factors', '0006_auto_20150414_1407'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factor',
            name='rating',
        ),
        migrations.AddField(
            model_name='factor',
            name='measure',
            field=models.ForeignKey(to='measures.Measure', null=True),
        ),
    ]
