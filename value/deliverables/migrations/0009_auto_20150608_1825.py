# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliverables', '0008_auto_20150608_1514'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rationale',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='rationale',
            name='object_id',
        ),
    ]
