# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0004_auto_20150413_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factor',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 14, 8, 21, 41, 760855, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
