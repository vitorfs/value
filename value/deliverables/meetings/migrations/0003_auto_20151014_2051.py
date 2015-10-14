# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0002_meeting_rationales_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(default=b'O', max_length=1, choices=[(b'O', b'Ongoing'), (b'A', b'Analysing'), (b'C', b'Closed')]),
        ),
    ]
