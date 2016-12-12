# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtime', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='station',
            old_name='data_date_regexp',
            new_name='data_date_format',
        ),
        migrations.RenameField(
            model_name='station',
            old_name='data_time_regexp',
            new_name='data_time_format',
        ),
    ]
