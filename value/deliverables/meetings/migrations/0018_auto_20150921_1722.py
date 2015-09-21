# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0017_auto_20150917_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scenario',
            name='meeting',
            field=models.ForeignKey(related_name='scenarios', to='meetings.Meeting'),
        ),
    ]
