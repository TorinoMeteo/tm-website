# Generated by Django 2.2.1 on 2020-12-17 16:06

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('realtime', '0017_auto_20190529_1040'),
    ]

    operations = [
        migrations.CreateModel(
            name='AirQualityStation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='nome')),
                ('slug', models.SlugField(max_length=128, verbose_name='slug')),
                ('short_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='nome abbreviato')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='descrizione')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='indirizzo')),
                ('city', models.CharField(blank=True, max_length=255, null=True, verbose_name='città/comune')),
                ('cap', models.CharField(blank=True, max_length=10, null=True, verbose_name='cap')),
                ('lat', models.CharField(max_length=255, verbose_name='latitudine')),
                ('lng', models.CharField(max_length=255, verbose_name='longitudine')),
                ('elevation', models.IntegerField(blank=True, null=True, verbose_name='altitudine')),
                ('active', models.BooleanField(default=True, verbose_name='attiva')),
                ('nation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='realtime.Nation', verbose_name='nazione')),
                ('province', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='realtime.Province', verbose_name='provincia')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='realtime.Region', verbose_name='regione')),
            ],
            options={
                'verbose_name': "stazione qualità dell'aria",
                'verbose_name_plural': "stazioni qualità dell'aria",
                'ordering': ('name',),
            },
        ),
    ]
