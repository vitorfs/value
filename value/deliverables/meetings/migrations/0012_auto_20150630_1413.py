# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0011_meetingitem_value_ranking'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meetingitem',
            options={'ordering': ('-value_ranking',)},
        ),
    ]
