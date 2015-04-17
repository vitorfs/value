# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0003_instanceitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='instance',
            name='has_backlog',
            field=models.BooleanField(default=False),
        ),
    ]
