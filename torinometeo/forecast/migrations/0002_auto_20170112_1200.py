# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor_uploader.fields


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayforecast',
            name='temperatures',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name=b'temperature'),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name=b'tempo previsto'),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='winds',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name=b'venti'),
        ),
        migrations.AlterField(
            model_name='forecast',
            name='pattern',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name=b'situazione'),
        ),
    ]
