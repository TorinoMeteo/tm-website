# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtime', '0009_auto_20170705_1357'),
    ]

    operations = [
        migrations.CreateModel(
            name='RadarConvertParams',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('param_name', models.CharField(max_length=50, verbose_name=b'nome parametro')),
                ('param_value', models.CharField(max_length=50, verbose_name=b'valore parametro')),
            ],
            options={
                'verbose_name': 'Parametri comando convert',
                'verbose_name_plural': 'Parametri comando convert',
            },
        ),
    ]
