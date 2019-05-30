# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('realtime', '0006_auto_20170112_1200'),
    ]

    operations = [
        migrations.CreateModel(
            name='StationBookmark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('insertion_date', models.DateTimeField(auto_now_add=True, verbose_name=b'inserimento')),
                ('station', models.ForeignKey(verbose_name=b'stazione', to='realtime.Station', on_delete=models.CASCADE)),
                ('user', models.ForeignKey(related_name='station_bookmarks', verbose_name=b'utente', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Bookmark',
                'verbose_name_plural': 'Bookmarks',
            },
        ),
    ]
