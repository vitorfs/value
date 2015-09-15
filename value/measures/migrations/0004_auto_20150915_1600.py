# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measures', '0003_auto_20150915_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measure',
            name='name',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
