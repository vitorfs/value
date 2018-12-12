# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-11-28 15:53
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0014_create_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='survey_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]