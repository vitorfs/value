# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliverables', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='decisionitemlookup',
            name='id',
        ),
        migrations.AlterField(
            model_name='decisionitemlookup',
            name='column_name',
            field=models.CharField(default='column', max_length=255, serialize=False, primary_key=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='decisionitemlookup',
            name='column_type',
            field=models.CharField(default='S', max_length=1, choices=[('S', 'String'), ('F', 'Float'), ('I', 'Integer'), ('D', 'Date'), ('T', 'Date Time')]),
        ),
    ]
