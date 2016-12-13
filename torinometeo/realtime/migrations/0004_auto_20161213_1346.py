# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtime', '0003_auto_20161213_1343'),
    ]

    operations = [
        migrations.RenameField(
            model_name='station',
            old_name='data_type',
            new_name='data_format',
        ),
    ]
