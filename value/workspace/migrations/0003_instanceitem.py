# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0002_auto_20150414_1407'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstanceItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('instance', models.ForeignKey(to='workspace.Instance')),
            ],
        ),
    ]
