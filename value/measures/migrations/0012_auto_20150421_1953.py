# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measures', '0011_auto_20150421_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurevalue',
            name='color',
            field=models.CharField(default='#32CD32', max_length=7, null=True, blank=True, choices=[('#A0522D', 'sienna'), ('#CD5C5C', 'indianred'), ('#FF4500', 'orangered'), ('#008B8B', 'darkcyan'), ('#B8860B', 'darkgoldenrod'), ('#32CD32', 'limegreen'), ('#FFD700', 'gold'), ('#48D1CC', 'mediumturquoise'), ('#87CEEB', 'skyblue'), ('#FF69B4', 'hotpink'), ('#CD5C5C', 'indianred'), ('#87CEFA', 'lightskyblue'), ('#6495ED', 'cornflowerblue'), ('#DC143C', 'crimson'), ('#FF8C00', 'darkorange'), ('#C71585', 'mediumvioletred'), ('#000000', 'black')]),
        ),
    ]
