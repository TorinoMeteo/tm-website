# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stationbookmark',
            options={'verbose_name': 'Bookmark Stazione', 'verbose_name_plural': 'Bookmarks Stazioni'},
        ),
        migrations.AlterField(
            model_name='stationbookmark',
            name='station',
            field=models.ForeignKey(related_name='bookmarks', verbose_name=b'stazione', to='realtime.Station'),
        ),
    ]
