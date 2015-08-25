# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliverables', '0011_decisionitemattachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='decisionitemattachment',
            name='decision_item',
            field=models.ForeignKey(related_name='attachments', to='deliverables.DecisionItem'),
        ),
    ]
