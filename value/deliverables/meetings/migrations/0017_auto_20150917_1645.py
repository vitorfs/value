# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0016_meetingitem_meeting_decision'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scenario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=14, choices=[(b'FACTORS', b'Factors Comparison'), (b'FACTORS_GROUPS', b'Factors Groups Comparison'), (b'ACCEPTANCE', b'Decision Items Acceptance')])),
                ('meeting', models.ForeignKey(to='meetings.Meeting')),
                ('meeting_items', models.ManyToManyField(to='meetings.MeetingItem')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='scenario',
            unique_together=set([('name', 'meeting', 'category')]),
        ),
    ]
