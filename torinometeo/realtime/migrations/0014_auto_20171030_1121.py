# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtime', '0013_forecastweather'),
    ]

    operations = [
        migrations.AddField(
            model_name='forecastweather',
            name='text',
            field=models.CharField(default='', max_length=50, verbose_name=b'testo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='weather',
            name='text',
            field=models.CharField(default='', max_length=50, verbose_name=b'testo'),
            preserve_default=False,
        ),
    ]
