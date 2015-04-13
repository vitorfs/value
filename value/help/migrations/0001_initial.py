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
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
                ('description', models.TextField()),
                ('category', models.CharField(max_length=2, choices=[('A', 'Administrator Functions'), ('G', 'General Usage')])),
                ('is_active', models.BooleanField(default=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='article_creation_user', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(related_name='article_update_user', to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
