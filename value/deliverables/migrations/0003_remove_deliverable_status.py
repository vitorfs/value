# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliverables', '0002_auto_20150520_1530'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliverable',
            name='status',
        ),
    ]
