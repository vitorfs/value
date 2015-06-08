# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deliverables', '0007_auto_20150603_1800'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rationale',
            old_name='reasoning',
            new_name='text',
        ),
    ]
