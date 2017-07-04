# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import colorful.fields


class Migration(migrations.Migration):

    dependencies = [
        ('realtime', '0007_radarsnapshot'),
    ]

    operations = [
        migrations.CreateModel(
            name='RadarColorConversion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('original_color', models.CharField(help_text=b'formato hex, i.e #ff8090', max_length=7, verbose_name=b'colore iniziale')),
                ('converted_color', colorful.fields.RGBColorField(verbose_name=b'colore finale')),
                ('tolerance', models.IntegerField(verbose_name=b'tolleranza')),
            ],
            options={
                'verbose_name': 'Conversione colore radar',
                'verbose_name_plural': 'Conversioni colori radar',
            },
        ),
    ]
