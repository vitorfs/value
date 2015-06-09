# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0007_auto_20150608_1825'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='decision_items',
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='stakeholders',
        ),
    ]
