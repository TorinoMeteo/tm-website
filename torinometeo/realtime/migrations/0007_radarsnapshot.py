# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtime', '0006_auto_20170112_1200'),
    ]

    operations = [
        migrations.CreateModel(
            name='RadarSnapshot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(verbose_name=b'data e ora')),
                ('filename', models.CharField(max_length=128, verbose_name=b'nome file')),
            ],
            options={
                'verbose_name': 'Immagine radar',
                'verbose_name_plural': 'Immagini radar',
            },
        ),
    ]
