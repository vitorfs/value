# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meetingstakeholder',
            options={'ordering': ('stakeholder__first_name', 'stakeholder__last_name', 'stakeholder__username')},
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='ended_at',
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='started_at',
        ),
        migrations.AddField(
            model_name='evaluation',
            name='reasoning',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meeting',
            name='date_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meeting',
            name='status',
            field=models.CharField(default='O', max_length=1, choices=[('O', 'Ongoing'), ('F', 'Finished')]),
        ),
    ]
