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
            name='Instance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=2000, null=True, blank=True)),
                ('status', models.CharField(default='I', max_length=1, choices=[('I', 'Initialized'), ('R', 'Running'), ('F', 'Finished')])),
                ('has_backlog', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(related_name='instance_creation_user', to=settings.AUTH_USER_MODEL)),
                ('manager', models.ForeignKey(related_name='instance_manager_user', to=settings.AUTH_USER_MODEL)),
                ('stakeholders', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(related_name='instance_update_user', to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='InstanceItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('instance', models.ForeignKey(to='workspace.Instance')),
            ],
        ),
    ]
