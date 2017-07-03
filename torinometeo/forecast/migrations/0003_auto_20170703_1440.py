# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0002_auto_20170112_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='dayforecast',
            name='note',
            field=models.TextField(null=True, verbose_name=b'note', blank=True),
        ),
        migrations.AddField(
            model_name='forecast',
            name='note',
            field=models.TextField(null=True, verbose_name=b'note', blank=True),
        ),
    ]
