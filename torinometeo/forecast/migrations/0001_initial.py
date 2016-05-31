# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import forecast.models
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DayForecast',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(unique=True, verbose_name=b'data')),
                ('image12', models.ImageField(upload_to=forecast.models.set_forecast_image_folder, verbose_name=b'immagine 0-12')),
                ('image24', models.ImageField(upload_to=forecast.models.set_forecast_image_folder, verbose_name=b'immagine 12-24')),
                ('text', ckeditor.fields.RichTextField(verbose_name=b'tempo previsto')),
                ('temperatures', ckeditor.fields.RichTextField(verbose_name=b'temperature')),
                ('winds', ckeditor.fields.RichTextField(verbose_name=b'venti')),
                ('reliability', models.IntegerField(verbose_name=b'attendibilit\xc3\xa0')),
            ],
            options={
                'ordering': ('date',),
                'verbose_name': 'previsioni giornata',
                'verbose_name_plural': 'previsioni giornate',
            },
        ),
        migrations.CreateModel(
            name='Forecast',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(unique=True, verbose_name=b'data')),
                ('pattern', ckeditor.fields.RichTextField(verbose_name=b'situazione')),
            ],
            options={
                'verbose_name': 'previsione',
                'verbose_name_plural': 'previsioni',
            },
        ),
        migrations.AddField(
            model_name='dayforecast',
            name='forecast',
            field=models.ForeignKey(verbose_name=b'previsione', to='forecast.Forecast'),
        ),
    ]
