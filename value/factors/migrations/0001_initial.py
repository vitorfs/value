# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('measures', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Factor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('description', models.TextField(max_length=2000, null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('group', 'name'),
                'db_table': 'factors',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'db_table': 'factors_groups',
            },
        ),
        migrations.AddField(
            model_name='factor',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='factors.Group', null=True),
        ),
        migrations.AddField(
            model_name='factor',
            name='measure',
            field=models.ForeignKey(blank=True, to='measures.Measure', null=True),
        ),
    ]
