# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import colorful.fields


class Migration(migrations.Migration):

    dependencies = [
        ('realtime', '0008_radarcolorconversion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='radarcolorconversion',
            name='original_color',
            field=colorful.fields.RGBColorField(verbose_name=b'colore iniziale'),
        ),
    ]
