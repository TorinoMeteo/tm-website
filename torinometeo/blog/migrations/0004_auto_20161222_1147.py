# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20161222_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 22, 11, 47, 37, 425933), verbose_name=b'creazione'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='last_edit_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 22, 11, 47, 37, 425963), verbose_name=b'ultima modifica'),
        ),
    ]
