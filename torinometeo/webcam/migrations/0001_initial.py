# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import webcam.models
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BestShot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('caption', models.CharField(max_length=255, null=True, verbose_name=b'caption', blank=True)),
                ('image', models.ImageField(upload_to=webcam.models.set_webcam_image_folder, verbose_name=b'immagine')),
            ],
        ),
        migrations.CreateModel(
            name='Webcam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name=b'nome')),
                ('slug', models.SlugField(unique=True, max_length=128)),
                ('technology', models.CharField(max_length=128, verbose_name=b'tecnologia')),
                ('description', ckeditor.fields.RichTextField(null=True, verbose_name=b'descrizione', blank=True)),
                ('url', models.URLField(verbose_name=b'url')),
                ('active', models.BooleanField(default=True, verbose_name=b'attiva')),
            ],
            options={
                'verbose_name': 'webcam',
            },
        ),
        migrations.AddField(
            model_name='bestshot',
            name='webcam',
            field=models.ForeignKey(verbose_name=b'webcam', to='webcam.Webcam'),
        ),
    ]
