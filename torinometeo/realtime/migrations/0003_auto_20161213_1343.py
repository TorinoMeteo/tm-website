# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtime', '0002_auto_20161209_1630'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='weather',
        ),
        migrations.AlterField(
            model_name='station',
            name='data_date_format',
            field=models.CharField(max_length=128, null=True, verbose_name=b'formato data (python)', blank=True),
        ),
        migrations.AlterField(
            model_name='station',
            name='data_time_format',
            field=models.CharField(max_length=128, null=True, verbose_name=b'formato ora (python)', blank=True),
        ),
    ]
