# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workspace', '0008_meeting'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeetingItems',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('meeting_decision', models.NullBooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='instanceitem',
            name='column_1',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='instanceitem',
            name='column_10',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='instanceitem',
            name='column_11',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='instanceitem',
            name='column_12',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='instanceitem',
            name='column_13',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='instanceitem',
            name='column_14',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='instanceitem',
            name='column_15',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='instanceitem',
            name='column_16',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='instanceitem',
            name='column_17',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='instanceitem',
            name='column_18',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='instanceitem',
            name='column_19',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='instanceitem',
            name='column_2',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='instanceitem',
            name='column_20',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='instanceitem',
            name='column_3',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='instanceitem',
            name='column_4',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='instanceitem',
            name='column_5',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='instanceitem',
            name='column_6',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='instanceitem',
            name='column_7',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='instanceitem',
            name='column_8',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='instanceitem',
            name='column_9',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='instanceitem',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 11, 11, 18, 57, 645158, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='instanceitem',
            name='created_by',
            field=models.ForeignKey(related_name='deliverable_item_creation_user', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='instanceitem',
            name='description',
            field=models.CharField(max_length=2000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='instanceitem',
            name='final_decision',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='instanceitem',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 11, 11, 19, 11, 416241, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='instanceitem',
            name='updated_by',
            field=models.ForeignKey(related_name='deliverable_item_update_user', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='meetingitems',
            name='decision_item',
            field=models.ForeignKey(to='workspace.InstanceItem'),
        ),
        migrations.AddField(
            model_name='meetingitems',
            name='meeting',
            field=models.ForeignKey(to='workspace.Meeting'),
        ),
    ]
