# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0023_auto_20150928_2337'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ranking',
            options={'ordering': ('measure_value__order',)},
        ),
        migrations.AlterField(
            model_name='scenario',
            name='meeting_items',
            field=models.ManyToManyField(related_name='scenarios', to='meetings.MeetingItem'),
        ),
    ]
