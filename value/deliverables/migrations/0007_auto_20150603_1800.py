# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliverables', '0006_rationale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='decisionitem',
            name='description',
            field=models.TextField(max_length=2000, null=True, blank=True),
        ),
    ]
