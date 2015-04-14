# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='valuemodel',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 14, 8, 21, 58, 135175, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
