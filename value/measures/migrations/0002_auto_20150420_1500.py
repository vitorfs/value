# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measures', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='measurevalue',
            options={'ordering': ('-order',)},
        ),
        migrations.RemoveField(
            model_name='measurevalue',
            name='weight',
        ),
        migrations.AddField(
            model_name='measurevalue',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
