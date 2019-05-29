# Generated by Django 2.2.1 on 2019-05-29 08:40

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import forecast.models


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0004_forecast_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayforecast',
            name='date',
            field=models.DateField(unique=True, verbose_name='data'),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='forecast',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forecast.Forecast', verbose_name='previsione'),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='image12',
            field=models.ImageField(upload_to=forecast.models.set_forecast_image_folder, verbose_name='immagine 0-12'),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='image24',
            field=models.ImageField(upload_to=forecast.models.set_forecast_image_folder, verbose_name='immagine 12-24'),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='note',
            field=models.TextField(blank=True, null=True, verbose_name='note'),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='reliability',
            field=models.IntegerField(verbose_name='attendibilità'),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='temperatures',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='temperature'),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='tempo previsto'),
        ),
        migrations.AlterField(
            model_name='dayforecast',
            name='winds',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='venti'),
        ),
        migrations.AlterField(
            model_name='forecast',
            name='date',
            field=models.DateField(unique=True, verbose_name='data'),
        ),
        migrations.AlterField(
            model_name='forecast',
            name='note',
            field=models.TextField(blank=True, null=True, verbose_name='note'),
        ),
        migrations.AlterField(
            model_name='forecast',
            name='pattern',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='situazione'),
        ),
        migrations.AlterField(
            model_name='forecast',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='utente'),
        ),
    ]
