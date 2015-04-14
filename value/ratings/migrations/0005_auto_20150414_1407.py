# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0004_auto_20150414_0822'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='creation_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='rating',
            old_name='update_date',
            new_name='updated_at',
        ),
    ]
