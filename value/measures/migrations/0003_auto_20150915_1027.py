# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measures', '0002_auto_20150910_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurevalue',
            name='color',
            field=models.CharField(default=b'#337BB7', max_length=7, choices=[(b'#5CB85C', b'#5CB85C'), (b'#BAE8BA', b'#BAE8BA'), (b'#8AD38A', b'#8AD38A'), (b'#369836', b'#369836'), (b'#1B7C1B', b'#1B7C1B'), (b'#F0AD4E', b'#F0AD4E'), (b'#FFD8A0', b'#FFD8A0'), (b'#FFC675', b'#FFC675'), (b'#DE9226', b'#DE9226'), (b'#AD6D11', b'#AD6D11'), (b'#D9534F', b'#D9534F'), (b'#FFADAB', b'#FFADAB'), (b'#FC827F', b'#FC827F'), (b'#BE2F2B', b'#BE2F2B'), (b'#961512', b'#961512'), (b'#5BC1DE', b'#5BC1DE'), (b'#BAEAF8', b'#BAEAF8'), (b'#85D5EC', b'#85D5EC'), (b'#39ACCD', b'#39ACCD'), (b'#1993B6', b'#1993B6'), (b'#337BB7', b'#337BB7'), (b'#7EB1DC', b'#7EB1DC'), (b'#5393C8', b'#5393C8'), (b'#1265AB', b'#1265AB'), (b'#094B83', b'#094B83'), (b'#222222', b'#222222'), (b'#929191', b'#929191'), (b'#5E5E5E', b'#5E5E5E'), (b'#000000', b'#000000'), (b'#030202', b'#030202')]),
        ),
        migrations.AlterField(
            model_name='measurevalue',
            name='description',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='measurevalue',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
