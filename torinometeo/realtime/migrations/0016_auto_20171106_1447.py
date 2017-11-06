# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtime', '0015_auto_20171106_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stationforecast',
            name='last_edit',
            field=models.DateTimeField(verbose_name=b'ultima modifica'),
        ),
    ]
