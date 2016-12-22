# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20160628_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 22, 11, 46, 42, 616749), verbose_name=b'creazione'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='last_edit_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 22, 11, 46, 42, 616777), verbose_name=b'ultima modifica'),
        ),
    ]
