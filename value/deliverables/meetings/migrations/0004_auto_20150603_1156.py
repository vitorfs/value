# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0003_auto_20150528_1024'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meeting',
            options={'ordering': ('-updated_at',)},
        ),
        migrations.AlterUniqueTogether(
            name='evaluation',
            unique_together=set([('meeting', 'meeting_item', 'user', 'factor', 'measure')]),
        ),
    ]
