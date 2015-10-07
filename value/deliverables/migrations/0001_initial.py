# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import value.deliverables.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('measures', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('factors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DecisionItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=2000, null=True, blank=True)),
                ('column_1', models.CharField(max_length=255, null=True, blank=True)),
                ('column_2', models.CharField(max_length=255, null=True, blank=True)),
                ('column_3', models.CharField(max_length=255, null=True, blank=True)),
                ('column_4', models.CharField(max_length=255, null=True, blank=True)),
                ('column_5', models.CharField(max_length=255, null=True, blank=True)),
                ('column_6', models.CharField(max_length=255, null=True, blank=True)),
                ('column_7', models.CharField(max_length=255, null=True, blank=True)),
                ('column_8', models.CharField(max_length=255, null=True, blank=True)),
                ('column_9', models.CharField(max_length=255, null=True, blank=True)),
                ('column_10', models.CharField(max_length=255, null=True, blank=True)),
                ('column_11', models.CharField(max_length=255, null=True, blank=True)),
                ('column_12', models.CharField(max_length=255, null=True, blank=True)),
                ('column_13', models.CharField(max_length=255, null=True, blank=True)),
                ('column_14', models.CharField(max_length=255, null=True, blank=True)),
                ('column_15', models.CharField(max_length=255, null=True, blank=True)),
                ('column_16', models.CharField(max_length=255, null=True, blank=True)),
                ('column_17', models.CharField(max_length=255, null=True, blank=True)),
                ('column_18', models.CharField(max_length=255, null=True, blank=True)),
                ('column_19', models.CharField(max_length=255, null=True, blank=True)),
                ('column_20', models.CharField(max_length=255, null=True, blank=True)),
                ('column_21', models.CharField(max_length=255, null=True, blank=True)),
                ('column_22', models.CharField(max_length=255, null=True, blank=True)),
                ('column_23', models.CharField(max_length=255, null=True, blank=True)),
                ('column_24', models.CharField(max_length=255, null=True, blank=True)),
                ('column_25', models.CharField(max_length=255, null=True, blank=True)),
                ('column_26', models.CharField(max_length=255, null=True, blank=True)),
                ('column_27', models.CharField(max_length=255, null=True, blank=True)),
                ('column_28', models.CharField(max_length=255, null=True, blank=True)),
                ('column_29', models.CharField(max_length=255, null=True, blank=True)),
                ('column_30', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'db_table': 'decision_items',
            },
        ),
        migrations.CreateModel(
            name='DecisionItemAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attachment', models.FileField(upload_to=value.deliverables.models.attachment_file_upload_to)),
                ('decision_item', models.ForeignKey(related_name='attachments', to='deliverables.DecisionItem')),
            ],
        ),
        migrations.CreateModel(
            name='DecisionItemLookup',
            fields=[
                ('column_name', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('column_label', models.CharField(max_length=255, null=True, blank=True)),
                ('column_type', models.CharField(default=b'S', max_length=1, choices=[(b'S', b'String'), (b'F', b'Float'), (b'I', b'Integer'), (b'D', b'Date'), (b'T', b'Date Time')])),
                ('column_display', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'decision_items_lookup',
            },
        ),
        migrations.CreateModel(
            name='Deliverable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=2000, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(related_name='deliverable_creation_user', to=settings.AUTH_USER_MODEL)),
                ('factors', models.ManyToManyField(related_name='deliverables', to='factors.Factor')),
                ('manager', models.ForeignKey(related_name='deliverable_manager_user', to=settings.AUTH_USER_MODEL)),
                ('measure', models.ForeignKey(related_name='deliverables', to='measures.Measure')),
                ('stakeholders', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(related_name='deliverable_update_user', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'db_table': 'deliverables',
            },
        ),
        migrations.CreateModel(
            name='Rationale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(max_length=4000, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'rationales',
            },
        ),
        migrations.AddField(
            model_name='decisionitem',
            name='deliverable',
            field=models.ForeignKey(to='deliverables.Deliverable'),
        ),
    ]
