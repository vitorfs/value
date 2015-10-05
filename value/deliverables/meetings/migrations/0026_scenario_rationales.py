# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliverables', '0015_auto_20151005_1445'),
        ('meetings', '0025_auto_20151001_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenario',
            name='rationales',
            field=models.ManyToManyField(to='deliverables.Rationale'),
        ),
    ]
