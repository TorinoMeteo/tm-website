# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='related_entries',
            field=models.ManyToManyField(related_name='_related_entries_+', verbose_name=b'articoli correlati', to='blog.Entry', blank=True),
        ),
    ]
