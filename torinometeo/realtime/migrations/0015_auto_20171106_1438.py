# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtime', '0014_auto_20171030_1121'),
    ]

    operations = [
        migrations.CreateModel(
            name='StationForecast',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_edit', models.DateTimeField(auto_now=True, verbose_name=b'ultima modifica')),
                ('date', models.DateField(verbose_name=b'data')),
                ('period', models.IntegerField(verbose_name=b'periodo', choices=[(0, b'00:00 06:00'), (1, b'06:00 12:00'), (2, b'12:00 18:00'), (3, b'18:00 24:00')])),
                ('icon', models.CharField(max_length=255, verbose_name=b'icona')),
                ('text', models.CharField(max_length=50, verbose_name=b'testo')),
                ('data', models.TextField(verbose_name=b'json data')),
                ('station', models.ForeignKey(verbose_name=b'stazione', to='realtime.Station', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Previsione',
                'verbose_name_plural': 'Previsioni',
            },
        ),
        migrations.RemoveField(
            model_name='forecastweather',
            name='station',
        ),
        migrations.RemoveField(
            model_name='weather',
            name='station',
        ),
        migrations.DeleteModel(
            name='ForecastWeather',
        ),
        migrations.DeleteModel(
            name='Weather',
        ),
    ]
