# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measures', '0001_initial'),
        ('meetings', '0008_auto_20150609_1207'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('raw_votes', models.IntegerField(default=0)),
                ('percentage_votes', models.FloatField(default=0.0)),
                ('measure_value', models.ForeignKey(to='measures.MeasureValue')),
                ('meeting_item', models.ForeignKey(to='meetings.MeetingItem')),
            ],
        ),
    ]
