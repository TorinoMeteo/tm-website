# coding=utf-8
from django.db import models
from django.conf import settings
from django.utils import timezone

from ckeditor_uploader.fields import RichTextUploadingField
from colorful.fields import RGBColorField

from realtime.models.geo import Nation, Region, Province
from realtime.managers import StationManager

import datetime


def wind_dir_text_base(value): # noqa
    value = float(value)
    if value < 11:
        return 'N'
    elif value < 34:
        return 'NNE'
    elif value < 56:
        return 'NE'
    elif value < 79:
        return 'ENE'
    elif value < 101:
        return 'E'
    elif value < 124:
        return 'ESE'
    elif value < 146:
        return 'SE'
    elif value < 169:
        return 'SSE'
    elif value < 191:
        return 'S'
    elif value < 214:
        return 'SSO'
    elif value < 236:
        return 'SO'
    elif value < 259:
        return 'OSO'
    elif value < 281:
        return 'O'
    elif value < 304:
        return 'ONO'
    elif value < 326:
        return 'NO'
    elif value < 349:
        return 'NNO'
    elif value < 360:
        return 'N'
    else:
        return None


class DataFormat(models.Model):
    """ Data formats provided by stations
    """
    name = models.CharField('nome', max_length=64)
    description = models.TextField('descrizione')

    class Meta:
        verbose_name = 'Formato dati'
        verbose_name_plural = 'Formati dati'

    def __unicode__(self):
        return self.name


def set_station_image_folder(instance, filename):
    """ Path to the upload folder for station images
    """
    return '/'.join([settings.MEDIA_REALTIME_STATION_IMG_REL, filename])


class Station(models.Model):

    # range in seconds for data to be considered live
    RT_RANGE_SECONDS = 60 * 70

    """ Station model
    """
    name = models.CharField('nome', max_length=128)
    slug = models.SlugField('slug', max_length=128)
    short_name = models.CharField('nome abbreviato', max_length=64,
                                  null=True, blank=True)
    description = RichTextUploadingField('descrizione')
    climate = RichTextUploadingField('clima', blank=True, null=True)
    web = models.URLField('sito web', max_length=255, blank=True, null=True)
    webcam = models.URLField('webcam url', max_length=255,
                             blank=True, null=True)
    image = models.ImageField(upload_to=set_station_image_folder,
                              blank=True, null=True)
    nation = models.ForeignKey(Nation, verbose_name='nazione',
                               blank=True, null=True)
    region = models.ForeignKey(Region, verbose_name='regione',
                               blank=True, null=True)
    province = models.ForeignKey(Province, verbose_name='provincia',
                                 blank=True, null=True)
    address = models.CharField('indirizzo', max_length=255,
                               blank=True, null=True)
    city = models.CharField('città/comune', max_length=255,
                            blank=True, null=True)
    cap = models.CharField('cap', max_length=10, blank=True, null=True)
    lat = models.CharField('latitudine', max_length=255)
    lng = models.CharField('longitudine', max_length=255)
    elevation = models.IntegerField('altitudine')
    mean_year_rain = models.DecimalField('pioggia media annua',
                                         max_digits=8, decimal_places=1)
    station_model = models.CharField('modello stazione', max_length=255)
    software_model = models.CharField('software', max_length=255)
    installation_type = models.CharField('tipo intallazione', max_length=255)
    installation_position = models.CharField('posizionamento', max_length=255)
    elevation_ground = models.IntegerField('elevazione dal suolo')
    data_url = models.URLField('url dati', max_length=255)
    data_format = models.ForeignKey(DataFormat, verbose_name='formato dati')
    data_date_format = models.CharField('formato data (python)',
                                        max_length=128, null=True, blank=True)
    data_time_format = models.CharField('formato ora (python)',
                                        max_length=128, null=True, blank=True)
    forecast_url = models.URLField('url sito previsionale',
                                   max_length=255, null=True, blank=True)
    ranking = models.IntegerField('ranking', default=1)
    active = models.BooleanField('attiva', default=True)

    objects = StationManager()

    class Meta:
        verbose_name = 'stazione'
        verbose_name_plural = 'stazioni'
        ordering = ('name', )

    def __unicode__(self):
        return '%s' % self.name

    @models.permalink
    def get_absolute_url(self):
        return ('realtime-station', None, {
            'slug': self.slug,
        })

    def now(self):
        """ Returns the current datetime, for debug and dev purposes
        """
        return timezone.now()
        datetime_obj = datetime.datetime(2015, 03, 11, 10, 40, 00)
        return timezone.make_aware(datetime_obj,
                                   timezone.get_current_timezone())

    def get_realtime_data(self):
        """ Last measured data, if inside the Station.RT_RANGE_SECONDS range
            http://stackoverflow.com/questions/21918802/problems-filtering-django-datetime-field-by-month-and-day
        """
        date = self.now()
        try:
            data = Data.objects.filter(
                station=self.id,
                datetime__year=date.year,
                datetime__month=date.month,
                datetime__day=date.day).order_by('-id').first()
            time_difference = self.now() - data.datetime
            if(time_difference.total_seconds() > Station.RT_RANGE_SECONDS):
                return None

            return data
        except:
            return None

    def get_day_data(self):
        """ All data of the current day, @see self.now
        """
        date = self.now()
        day_data = {
            'temperature': [],
            'pressure': [],
            'relative_humidity': [],
            'rain_rate': [],
            'rain': []
        }

        data = Data.objects.filter(
            station=self.id,
            datetime__year=date.year,
            datetime__month=date.month,
            datetime__day=date.day).order_by('id').distinct()
        for record in data:
            datetime_data = {
                'datetime_year': record.datetime.year,
                'datetime_month': record.datetime.month,
                'datetime_day': record.datetime.day,
                'datetime_hour': record.datetime.hour,
                'datetime_minute': record.datetime.minute,
                'datetime_second': record.datetime.second,
            }
            temperature_data = datetime_data.copy()
            temperature_data.update({'value': record.temperature})
            day_data['temperature'].append(temperature_data)

            pressure_data = datetime_data.copy()
            pressure_data.update({'value': record.pressure})
            day_data['pressure'].append(pressure_data)

            relative_humidity_data = datetime_data.copy()
            relative_humidity_data.update({'value': record.relative_humidity})
            day_data['relative_humidity'].append(relative_humidity_data)

            rain_rate_data = datetime_data.copy()
            rain_rate_data.update({'value': record.rain_rate})
            day_data['rain_rate'].append(rain_rate_data)

            rain_data = datetime_data.copy()
            rain_data.update({'value': record.rain})
            day_data['rain'].append(rain_data)

        return day_data

    def get_last24_data(self):
        """ All data of the last 24 hours, @see self.now
        """
        date = self.now()
        day_data = {
            'temperature': [],
            'pressure': [],
            'relative_humidity': [],
            'rain_rate': [],
            'rain': []
        }

        date_from = date - datetime.timedelta(days=1)
        data = Data.objects.filter(
            station=self.id,
            datetime__gte=date_from).order_by('id').distinct()
        for record in data:
            datetime_data = {
                'datetime_year': record.datetime.year,
                'datetime_month': record.datetime.month,
                'datetime_day': record.datetime.day,
                'datetime_hour': record.datetime.hour,
                'datetime_minute': record.datetime.minute,
                'datetime_second': record.datetime.second,
            }
            temperature_data = datetime_data.copy()
            temperature_data.update({'value': record.temperature})
            day_data['temperature'].append(temperature_data)

            pressure_data = datetime_data.copy()
            pressure_data.update({'value': record.pressure})
            day_data['pressure'].append(pressure_data)

            relative_humidity_data = datetime_data.copy()
            relative_humidity_data.update({'value': record.relative_humidity})
            day_data['relative_humidity'].append(relative_humidity_data)

            rain_rate_data = datetime_data.copy()
            rain_rate_data.update({'value': record.rain_rate})
            day_data['rain_rate'].append(rain_rate_data)

            rain_data = datetime_data.copy()
            rain_data.update({'value': record.rain})
            day_data['rain'].append(rain_data)

        return day_data

    def get_historic_data(self, from_date, to_date):

        historic_data = []
        data = HistoricData.objects.filter(
            station=self.id,
            date__gte=from_date,
            date__lte=to_date).order_by('date').distinct()
        for record in data:
            historic_data.append({
                'date_obj': record.date,
                'date': record.date.strftime('%Y-%m-%d'),
                'temperature_mean': record.temperature_mean,
                'temperature_max': record.temperature_max,
                'temperature_min': record.temperature_min,
                'pressure_mean': record.pressure_mean,
                'pressure_max': record.pressure_max,
                'pressure_min': record.pressure_min,
                'relative_humidity_mean': record.relative_humidity_mean,
                'relative_humidity_max': record.relative_humidity_max,
                'relative_humidity_min': record.relative_humidity_min,
                'rain': record.rain
            })

        return historic_data

    def get_data_first_date(self):
        data = HistoricData.objects.filter(
            station=self.id).order_by('date').distinct()[0]
        return data.date


class Data(models.Model):
    """ Realtime data model class
    """
    station = models.ForeignKey(Station, verbose_name='stazione')
    datetime = models.DateTimeField('data e ora', auto_now=False,
                                    auto_now_add=False)
    temperature = models.DecimalField('temperatura', max_digits=3,
                                      decimal_places=1, blank=True, null=True)
    temperature_max = models.DecimalField(
        'temperatura massima', max_digits=3,
        decimal_places=1, blank=True, null=True)
    temperature_max_time = models.TimeField(
        'ora temperatura massima',
        blank=True, null=True)
    temperature_min = models.DecimalField(
        'temperatura minima', max_digits=3,
        decimal_places=1, blank=True, null=True)
    temperature_min_time = models.TimeField('ora temperatura minima',
                                            blank=True, null=True)
    relative_humidity = models.DecimalField(
        'umidità relativa', max_digits=4,
        decimal_places=1, blank=True, null=True)
    relative_humidity_max = models.DecimalField('umidità relativa massima',
                                                max_digits=4, decimal_places=1,
                                                blank=True, null=True)
    relative_humidity_max_time = models.TimeField(
        'ora umidità relativa massima', blank=True, null=True)
    relative_humidity_min = models.DecimalField(
        'umidità relativa minima', max_digits=4, decimal_places=1,
        blank=True, null=True)
    relative_humidity_min_time = models.TimeField(
        'ora umidità relativa minima', blank=True, null=True)
    dewpoint = models.DecimalField(
        'dewpoint', max_digits=3, decimal_places=1, blank=True, null=True)
    dewpoint_max = models.DecimalField(
        'dewpoint massima', max_digits=3, decimal_places=1,
        blank=True, null=True)
    dewpoint_max_time = models.TimeField(
        'ora dewpoint massima', blank=True, null=True)
    dewpoint_min = models.DecimalField(
        'dewpoint minima', max_digits=3, decimal_places=1,
        blank=True, null=True)
    dewpoint_min_time = models.TimeField(
        'ora dewpoint minima', blank=True, null=True)
    pressure = models.DecimalField(
        'pressione', max_digits=5, decimal_places=1, blank=True, null=True)
    pressure_max = models.DecimalField(
        'pressione massima', max_digits=5, decimal_places=1,
        blank=True, null=True)
    pressure_max_time = models.TimeField(
        'ora pressione massima', blank=True, null=True)
    pressure_min = models.DecimalField(
        'pressione minima', max_digits=5, decimal_places=1,
        blank=True, null=True)
    pressure_min_time = models.TimeField(
        'ora pressione minima', blank=True, null=True)
    wind_strength = models.DecimalField(
        'vento', max_digits=4, decimal_places=1, blank=True, null=True)
    wind_dir = models.CharField(
        'direzione vento', max_length=10, blank=True, null=True)
    wind_strength_max = models.DecimalField(
        'vento massimo', max_digits=4, decimal_places=1, blank=True, null=True)
    wind_dir_max = models.CharField(
        'direzione vento massimo', max_length=10, blank=True, null=True)
    wind_max_time = models.TimeField(
        'ora vento massimo', blank=True, null=True)
    rain = models.DecimalField(
        'accumulo precipitazioni', max_digits=8, decimal_places=1,
        blank=True, null=True)
    rain_rate = models.DecimalField(
        'rateo precipitazioni', max_digits=8, decimal_places=1,
        blank=True, null=True)
    rain_rate_max = models.DecimalField(
        'rateo massimo precipitazioni', max_digits=8, decimal_places=1,
        blank=True, null=True)
    rain_rate_max_time = models.TimeField('ora rateo massimo precipitazioni',
                                          blank=True, null=True)
    rain_month = models.DecimalField('accumulo mensile precipitazioni',
                                     max_digits=8, decimal_places=1,
                                     blank=True, null=True)
    rain_year = models.DecimalField(
        'accumulo annuale precipitazioni', max_digits=8, decimal_places=1,
        blank=True, null=True)

    class Meta:
        verbose_name = 'Dati realtime'
        verbose_name_plural = 'Dati realtime'

    def __unicode__(self):
        return '%s - %s' % (
            self.station.name,
            str(self.datetime) if self.datetime else '')

    @property
    def wind_dir_text(self):
        if self.wind_dir:
            try:
                return wind_dir_text_base(self.wind_dir)
            except:
                pass
        return ''

    @property
    def wind_dir_max_text(self):
        if self.wind_dir_max:
            try:
                return wind_dir_text_base(self.wind_dir_max)
            except:
                pass
        return ''


class HistoricData(models.Model):
    """ Historic data model class
    """
    station = models.ForeignKey(Station, verbose_name='stazione')
    date = models.DateField('data', auto_now=False, auto_now_add=False)
    temperature_max = models.DecimalField(
        'temperatura massima', max_digits=3, decimal_places=1,
        blank=True, null=True)
    temperature_min = models.DecimalField(
        'temperatura minima', max_digits=3, decimal_places=1,
        blank=True, null=True)
    temperature_mean = models.DecimalField(
        'temperatura media', max_digits=3, decimal_places=1,
        blank=True, null=True)
    relative_humidity_max = models.DecimalField(
        'umidità relativa massima', max_digits=4, decimal_places=1,
        blank=True, null=True)
    relative_humidity_min = models.DecimalField(
        'umidità relativa minima', max_digits=4, decimal_places=1,
        blank=True, null=True)
    relative_humidity_mean = models.DecimalField(
        'umidità relativa media', max_digits=4, decimal_places=1,
        blank=True, null=True)
    pressure_max = models.DecimalField(
        'pressione massima', max_digits=5, decimal_places=1,
        blank=True, null=True)
    pressure_min = models.DecimalField(
        'pressione minima', max_digits=5, decimal_places=1,
        blank=True, null=True)
    pressure_mean = models.DecimalField(
        'pressione media', max_digits=5, decimal_places=1,
        blank=True, null=True)
    rain = models.DecimalField(
        'accumulo precipitazioni', max_digits=8, decimal_places=1,
        blank=True, null=True)

    class Meta:
        verbose_name = 'Dati storici'
        verbose_name_plural = 'Dati storici'

    def __unicode__(self):
        return '%s - %s' % (self.station, self.date)


def set_net_request_image_folder(instance, filename):
    """ Path to the upload folder for station images
    """
    return '/'.join([settings.MEDIA_REALTIME_NET_REQUEST_IMG_REL, filename])


class NetRequest(models.Model):
    """ Net entrance request
    """
    date = models.DateTimeField('data', auto_now_add=True)
    firstname = models.CharField('nome', max_length=128)
    lastname = models.CharField('cognome', max_length=128)
    email = models.EmailField('e-mail', max_length=255)
    phone = models.CharField('telefono', max_length=64, blank=True, null=True)
    station_description = models.TextField('descrizione stazione')
    climate = models.TextField('microclima')
    web_site_url = models.URLField('URL sito web', max_length=255,
                                   blank=True, null=True)
    webcam_url = models.URLField('Webcam URL', max_length=255, blank=True,
                                 null=True)
    address = models.CharField('indirizzo', max_length=255)
    city = models.CharField('città', max_length=128)
    province = models.CharField('provincia', max_length=2)
    nation = models.CharField('nazione', max_length=128)
    lat = models.CharField('latitudine', max_length=128)
    lng = models.CharField('longitudine', max_length=128)
    elevation = models.IntegerField('altitudine')
    mean_year_rain = models.IntegerField('precipitazione media annua (mm)')
    station_model = models.CharField('modello stazione', max_length=255)
    software_model = models.CharField('modello software', max_length=255)
    installation_type = models.CharField('tipo di installazione',
                                         max_length=255)
    installation_position = models.CharField('ubicazione', max_length=255)
    elevation_ground = models.DecimalField('altezza dal suolo (m)',
                                           max_digits=5, decimal_places=2)
    data_url = models.URLField('URL dati realtime', blank=True, null=True)
    image = models.ImageField(upload_to=set_net_request_image_folder)

    class Meta:
        verbose_name = 'Richiesta ingresso nella rete'
        verbose_name_plural = 'Richieste ingresso nella rete'

    def __unicode__(self):
        return '%s %s - %s' % (self.firstname, self.lastname, self.city)


class RadarSnapshot(models.Model):
    datetime = models.DateTimeField('data e ora', auto_now=False, auto_now_add=False) # noqa
    filename = models.CharField('nome file', max_length=128)
    save_datetime = models.DateTimeField('salvataggio', auto_now=True)

    class Meta:
        verbose_name = "Immagine radar"
        verbose_name_plural = "Immagini radar"

    def __unicode__(self):
        return self.filename


class RadarColorConversion(models.Model):
    original_color = RGBColorField(verbose_name='colore iniziale')
    converted_color = RGBColorField(verbose_name='colore finale')
    tolerance = models.IntegerField('tolleranza')

    class Meta:
        verbose_name = "Conversione colore radar"
        verbose_name_plural = "Conversioni colori radar"

    def __unicode__(self):
        return '%s - %s' % (self.original_color, str(self.converted_color))


class RadarConvertParams(models.Model):
    param_name = models.CharField('nome parametro', max_length=50)
    param_value = models.CharField('valore parametro', max_length=50)

    class Meta:
        verbose_name = "Parametri comando convert"
        verbose_name_plural = "Parametri comando convert"

    def __unicode__(self):
        return '%s' % self.param_name
