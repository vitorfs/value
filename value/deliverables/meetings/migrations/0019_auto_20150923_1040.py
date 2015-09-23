# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0018_auto_20150921_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scenario',
            name='category',
            field=models.CharField(blank=True, max_length=14, null=True, choices=[(b'FACTORS', b'Factors Comparison'), (b'FACTORS_GROUPS', b'Factors Groups Comparison'), (b'ACCEPTANCE', b'Decision Items Acceptance')]),
        ),
    ]
