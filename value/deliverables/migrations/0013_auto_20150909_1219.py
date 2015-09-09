# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliverables', '0012_auto_20150825_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverable',
            name='factors',
            field=models.ManyToManyField(related_name='deliverables', to='factors.Factor'),
        ),
        migrations.AlterField(
            model_name='deliverable',
            name='measure',
            field=models.ForeignKey(related_name='deliverables', to='measures.Measure'),
        ),
    ]
