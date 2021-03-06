# Generated by Django 2.2.1 on 2021-01-27 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('realtime', '0022_auto_20201221_1038'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricAirQualityData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='data')),
                ('air_quality_index_max', models.DecimalField(decimal_places=1, max_digits=4, verbose_name="indice qualità dell'aria massimo")),
                ('air_quality_index_min', models.DecimalField(decimal_places=1, max_digits=4, verbose_name="indice qualità dell'aria minimo")),
                ('air_quality_index_mean', models.DecimalField(decimal_places=1, max_digits=4, verbose_name="indice qualità dell'aria medio")),
                ('pm1_max', models.DecimalField(decimal_places=1, max_digits=8, verbose_name='pm 1 massimo')),
                ('pm1_min', models.DecimalField(decimal_places=1, max_digits=8, verbose_name='pm 1 minimo')),
                ('pm1_mean', models.DecimalField(decimal_places=1, max_digits=8, verbose_name='pm 1 minimo')),
                ('pm25_max', models.DecimalField(decimal_places=1, max_digits=8, verbose_name='pm 2.5 massimo')),
                ('pm25_min', models.DecimalField(decimal_places=1, max_digits=8, verbose_name='pm 2.5 minimo')),
                ('pm25_mean', models.DecimalField(decimal_places=1, max_digits=8, verbose_name='pm 2.5 minimo')),
                ('pm10_max', models.DecimalField(decimal_places=1, max_digits=8, verbose_name='pm 10 massimo')),
                ('pm10_min', models.DecimalField(decimal_places=1, max_digits=8, verbose_name='pm 10 minimo')),
                ('pm10_mean', models.DecimalField(decimal_places=1, max_digits=8, verbose_name='pm 10 minimo')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historic_data', to='realtime.AirQualityStation', verbose_name='stazione')),
            ],
            options={
                'verbose_name': "Dati storici qualità dell'aria",
                'verbose_name_plural': "Dati storici qualità dell'aria",
            },
        ),
    ]
