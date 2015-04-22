# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factor',
            name='measure',
            field=models.ForeignKey(blank=True, to='measures.Measure', null=True),
        ),
    ]
