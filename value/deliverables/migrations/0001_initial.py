# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DecisionItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=2000, null=True, blank=True)),
                ('final_decision', models.NullBooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
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
                ('created_by', models.ForeignKey(related_name='decision_item_creation_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DecisionItemLookup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('column_name', models.CharField(max_length=255, unique=True, null=True, blank=True)),
                ('column_label', models.CharField(max_length=255, null=True, blank=True)),
                ('column_type', models.CharField(default='S', max_length=1, choices=[('B', 'Boolean'), ('S', 'String'), ('F', 'Float'), ('I', 'Integer'), ('D', 'Date'), ('T', 'Date Time')])),
            ],
        ),
        migrations.CreateModel(
            name='Deliverable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=2000, null=True, blank=True)),
                ('status', models.CharField(default='O', max_length=1, choices=[('O', 'Ongoing'), ('F', 'Finished')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(related_name='deliverable_creation_user', to=settings.AUTH_USER_MODEL)),
                ('manager', models.ForeignKey(related_name='deliverable_manager_user', to=settings.AUTH_USER_MODEL)),
                ('stakeholders', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(related_name='deliverable_update_user', to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='decisionitem',
            name='deliverable',
            field=models.ForeignKey(to='deliverables.Deliverable'),
        ),
        migrations.AddField(
            model_name='decisionitem',
            name='updated_by',
            field=models.ForeignKey(related_name='decision_item_update_user', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
