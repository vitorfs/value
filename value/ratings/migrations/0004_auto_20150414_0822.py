# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0003_auto_20150414_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 14, 8, 22, 5, 12507, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
