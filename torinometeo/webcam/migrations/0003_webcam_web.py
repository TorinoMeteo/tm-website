# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webcam', '0002_webcam_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='webcam',
            name='web',
            field=models.URLField(null=True, verbose_name=b'pagina dedicata', blank=True),
        ),
    ]
