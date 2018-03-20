# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forecast', '0003_auto_20170703_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='forecast',
            name='user',
            field=models.ForeignKey(verbose_name=b'utente', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
