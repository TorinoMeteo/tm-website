# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webcam', '0003_webcam_web'),
    ]

    operations = [
        migrations.AddField(
            model_name='webcam',
            name='latitude',
            field=models.CharField(default='', max_length=50, verbose_name=b'latitudine'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='webcam',
            name='longitude',
            field=models.CharField(default='', max_length=50, verbose_name=b'longitudine'),
            preserve_default=False,
        ),
    ]
