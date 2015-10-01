# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0024_auto_20150929_0942'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='scenario',
            unique_together=set([('name', 'meeting')]),
        ),
        migrations.RemoveField(
            model_name='scenario',
            name='category',
        ),
    ]
