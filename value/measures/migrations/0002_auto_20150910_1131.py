# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measures', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='measure',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='measure',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='measure',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='measure',
            name='updated_by',
        ),
    ]
