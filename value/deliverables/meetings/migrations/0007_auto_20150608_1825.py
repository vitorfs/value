# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliverables', '0009_auto_20150608_1825'),
        ('meetings', '0006_remove_evaluation_reasoning'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='rationale',
            field=models.OneToOneField(null=True, to='deliverables.Rationale'),
        ),
        migrations.AddField(
            model_name='meetingitem',
            name='rationales',
            field=models.ManyToManyField(to='deliverables.Rationale'),
        ),
    ]
