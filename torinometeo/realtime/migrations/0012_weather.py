# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtime', '0011_radarsnapshot_save_datetime'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_edit', models.DateTimeField(auto_now=True, verbose_name=b'ultima modifica')),
                ('last_updated', models.DateTimeField(verbose_name=b'ultimo aggiornamento')),
                ('icon', models.CharField(max_length=255, verbose_name=b'icona')),
                ('data', models.TextField(verbose_name=b'json data')),
                ('station', models.ForeignKey(verbose_name=b'stazione', to='realtime.Station', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Tempo corrente',
                'verbose_name_plural': 'Tempo corrente',
            },
        ),
    ]
