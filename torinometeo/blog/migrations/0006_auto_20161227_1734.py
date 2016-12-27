# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor_uploader.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20161222_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name=b'testo'),
        ),
    ]
