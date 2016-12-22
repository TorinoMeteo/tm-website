# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtime', '0004_auto_20161213_1346'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nation',
            options={'ordering': ('name',), 'verbose_name': 'nazione', 'verbose_name_plural': 'nazioni'},
        ),
        migrations.AlterModelOptions(
            name='province',
            options={'ordering': ('name',), 'verbose_name': 'provincia', 'verbose_name_plural': 'province'},
        ),
        migrations.AlterModelOptions(
            name='region',
            options={'ordering': ('name',), 'verbose_name': 'regione', 'verbose_name_plural': 'regioni'},
        ),
        migrations.AlterModelOptions(
            name='station',
            options={'ordering': ('name',), 'verbose_name': 'stazione', 'verbose_name_plural': 'stazioni'},
        ),
        migrations.AlterField(
            model_name='station',
            name='data_format',
            field=models.ForeignKey(verbose_name=b'formato dati', to='realtime.DataFormat'),
        ),
    ]
