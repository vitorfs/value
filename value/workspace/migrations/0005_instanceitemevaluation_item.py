# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0004_auto_20150427_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='instanceitemevaluation',
            name='item',
            field=models.ForeignKey(default=1, to='workspace.InstanceItem'),
            preserve_default=False,
        ),
    ]
