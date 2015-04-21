# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('factors', '0001_initial'),
        ('measures', '0012_auto_20150421_1953'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workspace', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstanceItemEvaluation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('evaluated_at', models.DateTimeField(auto_now=True)),
                ('factor', models.ForeignKey(to='factors.Factor')),
                ('instance', models.ForeignKey(to='workspace.Instance')),
                ('measure', models.ForeignKey(to='measures.Measure')),
                ('measure_value', models.ForeignKey(to='measures.MeasureValue')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
