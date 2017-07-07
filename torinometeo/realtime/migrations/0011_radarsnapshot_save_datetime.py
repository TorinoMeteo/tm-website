# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('realtime', '0010_radarconvertparams'),
    ]

    operations = [
        migrations.AddField(
            model_name='radarsnapshot',
            name='save_datetime',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 7, 17, 19, 51, 255485), verbose_name=b'salvataggio', auto_now=True),
            preserve_default=False,
        ),
    ]
