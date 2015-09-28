# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0021_auto_20150928_2305'),
    ]

    operations = [
        migrations.AddField(
            model_name='ranking',
            name='meeting',
            field=models.ForeignKey(default=4, to='meetings.Meeting'),
            preserve_default=False,
        ),
    ]
