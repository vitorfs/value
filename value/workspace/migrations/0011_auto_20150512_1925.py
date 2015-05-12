# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workspace', '0010_auto_20150511_2045'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeetingItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('meeting_decision', models.NullBooleanField()),
                ('decision_item', models.ForeignKey(to='workspace.InstanceItem')),
                ('meeting', models.ForeignKey(to='workspace.Meeting')),
            ],
        ),
        migrations.CreateModel(
            name='MeetingStakeholder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('meeting_input', models.FloatField(default=0.0)),
                ('meeting', models.ForeignKey(to='workspace.Meeting')),
                ('stakeholder', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='meetingitems',
            name='decision_item',
        ),
        migrations.RemoveField(
            model_name='meetingitems',
            name='meeting',
        ),
        migrations.AddField(
            model_name='decisionitemlookup',
            name='column_type',
            field=models.CharField(default='S', max_length=1, choices=[('B', 'Boolean'), ('S', 'String'), ('F', 'Float'), ('I', 'Integer'), ('D', 'Date'), ('T', 'Date Time')]),
        ),
        migrations.DeleteModel(
            name='MeetingItems',
        ),
    ]
