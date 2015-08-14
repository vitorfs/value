# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0012_auto_20150630_1413'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meetingitem',
            options={'ordering': ('decision_item__name',)},
        ),
    ]
