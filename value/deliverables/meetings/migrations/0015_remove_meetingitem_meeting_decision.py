# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0014_meetingitem_meeting_ranking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meetingitem',
            name='meeting_decision',
        ),
    ]
