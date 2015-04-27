# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0003_auto_20150427_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instanceitemevaluation',
            name='evaluated_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
