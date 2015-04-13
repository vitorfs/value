# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0003_factor_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factor',
            name='created_by',
            field=models.ForeignKey(related_name='factor_creation_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='factor',
            name='updated_by',
            field=models.ForeignKey(related_name='factor_update_user', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
