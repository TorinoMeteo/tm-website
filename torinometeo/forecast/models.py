# coding=utf-8
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Forecast(models.Model):
    """ Forecast
    A Forecast includes n DayForecast models, each one is a prevision
    for one day
    """
    user = models.ForeignKey(
        User, verbose_name='utente', blank=True, null=True)
    date = models.DateField(
        'data', auto_now=False, auto_now_add=False, unique=True)
    pattern = RichTextUploadingField('situazione')
    note = models.TextField('note', blank=True, null=True)

    class Meta:
        verbose_name = 'previsione'
        verbose_name_plural = 'previsioni'

    def __unicode__(self):
        return 'previsione del %s' % str(self.date)


def set_forecast_image_folder(instance, filename):
    """ Path to the upload folder for forecast images
    """
    return '/'.join([settings.MEDIA_FORECAST_IMG_REL, filename])


class DayForecast(models.Model):
    """ DayForecast
    One day prevision
    """
    forecast = models.ForeignKey(Forecast, verbose_name='previsione')
    date = models.DateField(
        'data', auto_now=False, auto_now_add=False, unique=True)
    image12 = models.ImageField(
        verbose_name='immagine 0-12',
        upload_to=set_forecast_image_folder,
        blank=False,
        null=False)
    image24 = models.ImageField(
        verbose_name='immagine 12-24',
        upload_to=set_forecast_image_folder,
        blank=False,
        null=False)
    text = RichTextUploadingField('tempo previsto')
    temperatures = RichTextUploadingField('temperature')
    winds = RichTextUploadingField('venti')
    reliability = models.IntegerField('attendibilità')
    note = models.TextField('note', blank=True, null=True)

    class Meta:
        verbose_name = 'previsioni giornata'
        verbose_name_plural = 'previsioni giornate'
        ordering = ('date', )

    def __unicode__(self):
        return 'previsione per il giorno %s' % str(self.date)
