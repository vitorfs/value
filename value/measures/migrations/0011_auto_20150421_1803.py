# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measures', '0010_measurevalue_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurevalue',
            name='color',
            field=models.CharField(max_length=7, null=True, blank=True),
        ),
    ]
