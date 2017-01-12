# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor_uploader.fields


class Migration(migrations.Migration):

    dependencies = [
        ('realtime', '0005_auto_20161222_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='station',
            name='ranking',
            field=models.IntegerField(default=1, verbose_name=b'ranking'),
        ),
        migrations.AlterField(
            model_name='station',
            name='climate',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name=b'clima', blank=True),
        ),
        migrations.AlterField(
            model_name='station',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name=b'descrizione'),
        ),
    ]
