# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-21 14:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0005_auto_20160321_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ranking',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='ranking',
            name='measure_value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='measures.MeasureValue'),
        ),
        migrations.AlterField(
            model_name='ranking',
            name='meeting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetings.Meeting'),
        ),
    ]
