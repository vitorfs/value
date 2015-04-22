# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measures', '0012_auto_20150421_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurevalue',
            name='color',
            field=models.CharField(default='#337BB7', max_length=7, null=True, blank=True, choices=[('#5CB85C', '#5CB85C'), ('#BAE8BA', '#BAE8BA'), ('#8AD38A', '#8AD38A'), ('#369836', '#369836'), ('#1B7C1B', '#1B7C1B'), ('#F0AD4E', '#F0AD4E'), ('#FFD8A0', '#FFD8A0'), ('#FFC675', '#FFC675'), ('#DE9226', '#DE9226'), ('#AD6D11', '#AD6D11'), ('#D9534F', '#D9534F'), ('#FFADAB', '#FFADAB'), ('#FC827F', '#FC827F'), ('#BE2F2B', '#BE2F2B'), ('#961512', '#961512'), ('#5BC1DE', '#5BC1DE'), ('#BAEAF8', '#BAEAF8'), ('#85D5EC', '#85D5EC'), ('#39ACCD', '#39ACCD'), ('#1993B6', '#1993B6'), ('#337BB7', '#337BB7'), ('#7EB1DC', '#7EB1DC'), ('#5393C8', '#5393C8'), ('#1265AB', '#1265AB'), ('#094B83', '#094B83'), ('#222222', '#222222'), ('#929191', '#929191'), ('#5E5E5E', '#5E5E5E'), ('#000000', '#000000'), ('#030202', '#030202')]),
        ),
    ]
