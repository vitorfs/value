# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('measures', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
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
            options={
                'db_table': 'evaluations',
            },
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=2000, null=True, blank=True)),
                ('location', models.CharField(max_length=50, null=True, blank=True)),
                ('status', models.CharField(default='O', max_length=1, choices=[('O', 'Ongoing'), ('C', 'Closed')])),
                ('started_at', models.DateTimeField()),
                ('ended_at', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(related_name='meetings_created', to=settings.AUTH_USER_MODEL)),
                ('deliverable', models.ForeignKey(to='deliverables.Deliverable')),
            ],
            options={
                'ordering': ('-updated_at',),
                'db_table': 'meetings',
            },
        ),
        migrations.CreateModel(
            name='MeetingItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('meeting_decision', models.BooleanField(default=False)),
                ('value_ranking', models.FloatField(default=0.0)),
                ('meeting_ranking', models.FloatField(default=0.0)),
                ('decision_item', models.ForeignKey(to='deliverables.DecisionItem')),
                ('meeting', models.ForeignKey(to='meetings.Meeting')),
            ],
            options={
                'ordering': ('decision_item__name',),
                'db_table': 'meeting_items',
            },
        ),
        migrations.CreateModel(
            name='MeetingStakeholder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('meeting_input', models.FloatField(default=0.0)),
                ('meeting', models.ForeignKey(to='meetings.Meeting')),
                ('stakeholder', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('stakeholder__first_name', 'stakeholder__last_name', 'stakeholder__username'),
                'db_table': 'meeting_stakeholders',
            },
        ),
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('raw_votes', models.IntegerField(default=0)),
                ('percentage_votes', models.FloatField(default=0.0)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('measure_value', models.ForeignKey(to='measures.MeasureValue')),
                ('meeting', models.ForeignKey(to='meetings.Meeting')),
            ],
            options={
                'ordering': ('measure_value__order',),
                'db_table': 'rankings',
            },
        ),
        migrations.CreateModel(
            name='Rationale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(max_length=4000, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(related_name='rationales_created', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(related_name='rationales_updated', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'db_table': 'rationales',
            },
        ),
        migrations.CreateModel(
            name='Scenario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('value_ranking', models.FloatField(default=0.0)),
                ('meeting', models.ForeignKey(related_name='scenarios', to='meetings.Meeting')),
                ('meeting_items', models.ManyToManyField(related_name='scenarios', to='meetings.MeetingItem')),
                ('rationales', models.ManyToManyField(to='meetings.Rationale')),
            ],
            options={
                'db_table': 'scenarios',
            },
        ),
        migrations.AddField(
            model_name='meetingitem',
            name='rationales',
            field=models.ManyToManyField(to='meetings.Rationale'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='rationales',
            field=models.ManyToManyField(to='meetings.Rationale'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='updated_by',
            field=models.ForeignKey(related_name='meetings_updated', to=settings.AUTH_USER_MODEL, null=True),
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
            name='rationale',
            field=models.OneToOneField(null=True, to='meetings.Rationale'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='scenario',
            unique_together=set([('name', 'meeting')]),
        ),
        migrations.AlterUniqueTogether(
            name='ranking',
            unique_together=set([('content_type', 'object_id', 'measure_value')]),
        ),
        migrations.AlterUniqueTogether(
            name='evaluation',
            unique_together=set([('meeting', 'meeting_item', 'user', 'factor', 'measure')]),
        ),
    ]
