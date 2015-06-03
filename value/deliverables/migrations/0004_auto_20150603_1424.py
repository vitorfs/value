# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0001_initial'),
        ('measures', '0001_initial'),
        ('deliverables', '0003_remove_deliverable_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverable',
            name='factors',
            field=models.ManyToManyField(to='factors.Factor'),
        ),
        migrations.AddField(
            model_name='deliverable',
            name='measure',
            field=models.ForeignKey(default=1, to='measures.Measure'),
            preserve_default=False,
        ),
    ]
