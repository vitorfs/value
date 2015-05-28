# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0002_auto_20150528_0932'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='date_time',
        ),
        migrations.AddField(
            model_name='meeting',
            name='description',
            field=models.CharField(max_length=2000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meeting',
            name='ended_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meeting',
            name='location',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meeting',
            name='started_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 28, 7, 24, 7, 457268, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(default='O', max_length=1, choices=[('O', 'Ongoing'), ('C', 'Closed')]),
        ),
    ]
