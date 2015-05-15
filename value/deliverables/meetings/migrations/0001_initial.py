# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('measures', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('deliverables', '0001_initial'),
        ('factors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('evaluated_at', models.DateTimeField(null=True, blank=True)),
                ('factor', models.ForeignKey(to='factors.Factor')),
                ('measure', models.ForeignKey(to='measures.Measure')),
                ('measure_value', models.ForeignKey(blank=True, to='measures.MeasureValue', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('started_at', models.DateTimeField(null=True, blank=True)),
                ('ended_at', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(related_name='meeting_creation_user', to=settings.AUTH_USER_MODEL)),
                ('deliverable', models.ForeignKey(to='deliverables.Deliverable')),
                ('updated_by', models.ForeignKey(related_name='meeting_update_user', to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MeetingItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('meeting_decision', models.NullBooleanField()),
                ('decision_item', models.ForeignKey(to='deliverables.DecisionItem')),
                ('meeting', models.ForeignKey(to='meetings.Meeting')),
            ],
        ),
        migrations.CreateModel(
            name='MeetingStakeholder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('meeting_input', models.FloatField(default=0.0)),
                ('meeting', models.ForeignKey(to='meetings.Meeting')),
                ('stakeholder', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='evaluation',
            name='meeting',
            field=models.ForeignKey(to='meetings.Meeting'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='meeting_item',
            field=models.ForeignKey(to='meetings.MeetingItem'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
