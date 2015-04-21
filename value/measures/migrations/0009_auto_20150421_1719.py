# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measures', '0008_auto_20150421_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurevalue',
            name='order',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]
