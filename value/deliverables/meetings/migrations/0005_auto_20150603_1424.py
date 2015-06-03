# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('deliverables', '0004_auto_20150603_1424'),
        ('meetings', '0004_auto_20150603_1156'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='decision_items',
            field=models.ManyToManyField(to='deliverables.DecisionItem'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='stakeholders',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
