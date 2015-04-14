# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ratings', '0002_rating_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='created_by',
            field=models.ForeignKey(related_name='rating_creation_user', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rating',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 14, 8, 3, 15, 485166, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rating',
            name='update_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='rating',
            name='updated_by',
            field=models.ForeignKey(related_name='rating_update_user', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
