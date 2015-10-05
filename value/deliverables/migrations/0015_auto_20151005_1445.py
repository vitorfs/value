# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliverables', '0014_auto_20150927_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rationale',
            name='text',
            field=models.TextField(max_length=4000, null=True, blank=True),
        ),
    ]
