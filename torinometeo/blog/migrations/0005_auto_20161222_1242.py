# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20161222_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'creazione'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='last_edit_date',
            field=models.DateTimeField(auto_now=True, verbose_name=b'ultima modifica'),
        ),
    ]
