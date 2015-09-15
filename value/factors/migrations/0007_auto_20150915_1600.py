# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0006_auto_20150910_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factor',
            name='name',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
