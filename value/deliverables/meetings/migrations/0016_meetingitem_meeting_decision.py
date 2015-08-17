# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0015_remove_meetingitem_meeting_decision'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetingitem',
            name='meeting_decision',
            field=models.BooleanField(default=False),
        ),
    ]
