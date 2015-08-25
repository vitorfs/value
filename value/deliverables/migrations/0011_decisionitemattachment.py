# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import value.deliverables.models


class Migration(migrations.Migration):

    dependencies = [
        ('deliverables', '0010_decisionitemlookup_column_display'),
    ]

    operations = [
        migrations.CreateModel(
            name='DecisionItemAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attachment', models.FileField(upload_to=value.deliverables.models.attachment_file_upload_to)),
                ('decision_item', models.ForeignKey(to='deliverables.DecisionItem')),
            ],
        ),
    ]
