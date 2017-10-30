# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtime', '0012_weather'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForecastWeather',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_edit', models.DateTimeField(auto_now=True, verbose_name=b'ultima modifica')),
                ('date', models.DateField(verbose_name=b'data')),
                ('icon', models.CharField(max_length=255, verbose_name=b'icona')),
                ('data', models.TextField(verbose_name=b'json data')),
                ('station', models.ForeignKey(verbose_name=b'stazione', to='realtime.Station')),
            ],
            options={
                'verbose_name': 'Previsione grafica',
                'verbose_name_plural': 'Previsioni grafiche',
            },
        ),
    ]
