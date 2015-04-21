# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measures', '0002_auto_20150420_1500'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='measurevalue',
            options={'ordering': ('order',)},
        ),
        migrations.AlterField(
            model_name='measurevalue',
            name='description',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
