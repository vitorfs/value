# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0005_auto_20150603_1424'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluation',
            name='reasoning',
        ),
    ]
