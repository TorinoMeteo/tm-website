# coding=utf-8
import datetime

import pytz
from ckeditor_uploader.fields import RichTextUploadingField
from colorful.fields import RGBColorField
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

from realtime.managers import StationManager, AirQualityStationManager
from realtime.models.geo import Nation, Province, Region


def wind_dir_text_base(value):  # noqa
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

    def __str__(self):
        return self.name


def set_station_image_folder(instance, filename):
    """ Path to the upload folder for station images
    """
    return '/'.join([settings.MEDIA_REALTIME_STATION_IMG_REL, filename])


class Station(models.Model):

    # range in seconds for data to be considered live
    RT_RANGE_SECONDS = 60 * 120
    """ Station model
    """
    name = models.CharField('nome', max_length=128)
    slug = models.SlugField('slug', max_length=128)
    short_name = models.CharField(
        'nome abbreviato', max_length=64, null=True, blank=True)
    description = RichTextUploadingField('descrizione')
    climate = RichTextUploadingField('clima', blank=True, null=True)
    web = models.URLField('sito web', max_length=255, blank=True, null=True)
    webcam = models.URLField(
        'webcam url', max_length=255, blank=True, null=True)
    image = models.ImageField(
        upload_to=set_station_image_folder, blank=True, null=True)
    nation = models.ForeignKey(
        Nation,
        verbose_name='nazione',
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    region = models.ForeignKey(
        Region,
        verbose_name='regione',
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    province = models.ForeignKey(
        Province,
        verbose_name='provincia',
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    address = models.CharField(
        'indirizzo', max_length=255, blank=True, null=True)
    city = models.CharField(
        'città/comune', max_length=255, blank=True, null=True)
    cap = models.CharField('cap', max_length=10, blank=True, null=True)
    lat = models.CharField('latitudine', max_length=255)
    lng = models.CharField('longitudine', max_length=255)
    elevation = models.IntegerField('altitudine')
    mean_year_rain = models.DecimalField(
        'pioggia media annua', max_digits=8, decimal_places=1)
    station_model = models.CharField('modello stazione', max_length=255)
    software_model = models.CharField('software', max_length=255)
    installation_type = models.CharField('tipo intallazione', max_length=255)
    installation_position = models.CharField('posizionamento', max_length=255)
    elevation_ground = models.IntegerField('elevazione dal suolo')
    data_url = models.URLField('url dati', max_length=255)
    data_token = models.CharField('token url dati', max_length=50, blank=True, null=True)
    data_format = models.ForeignKey(
        DataFormat, verbose_name='formato dati', on_delete=models.CASCADE)
    data_date_format = models.CharField(
        'formato data (python)', max_length=128, null=True, blank=True)
    data_time_format = models.CharField(
        'formato ora (python)', max_length=128, null=True, blank=True)
    forecast_url = models.URLField(
        'url sito previsionale', max_length=255, null=True, blank=True)
    ranking = models.IntegerField('ranking', default=1)
    active = models.BooleanField('attiva', default=True)

    objects = StationManager()

    class Meta:
        verbose_name = 'stazione'
        verbose_name_plural = 'stazioni'
        ordering = ('name', )

    def __str__(self):
        return '%s' % self.name

    def get_absolute_url(self):
        return reverse('realtime-station', kwargs={
            'slug': self.slug,
        })

    def now(self):
        """ Returns the current datetime, for debug and dev purposes
        """
        return timezone.now()
        # datetime_obj = datetime.datetime(2015, 03, 11, 10, 40, 00)
        # return timezone.make_aware(datetime_obj,
        #                           timezone.get_current_timezone())

    def forecast_url_credits(self):
        if self.forecast_url:
            return self.forecast_url.replace("forecast.xml", "")
        return ""

    def weather_icon(self, encode=False):
        now = datetime.datetime.now()
        if now.hour < 6:
            period = 0
        elif now.hour < 12:
            period = 1
        elif now.hour < 18:
            period = 2
        else:
            period = 3

        forecast = StationForecast.objects.filter(
            station=self.id, date=now.date(), period=period).first()

        if forecast:
            icon = '%s%s.png' % (settings.BASE_WEATHER_ICON_URL, forecast.icon)
            text = forecast.text
            # @TODO check, probably not needed anymore
            if encode:
                return {
                    'icon': icon.encode('utf-8'),
                    'text': text.encode('utf-8')
                }
            else:
                return {'icon': icon, 'text': text}
        else:
            return None

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
            if (time_difference.total_seconds() > Station.RT_RANGE_SECONDS):
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
            aux_datetime = timezone.localtime(record.datetime,
                                              pytz.timezone(
                                                  settings.TIME_ZONE))  # noqa
            datetime_data = {
                'datetime_year': aux_datetime.year,
                'datetime_month': aux_datetime.month,
                'datetime_day': aux_datetime.day,
                'datetime_hour': aux_datetime.hour,
                'datetime_minute': aux_datetime.minute,
                'datetime_second': aux_datetime.second,
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
            aux_datetime = timezone.localtime(record.datetime,
                                              pytz.timezone(
                                                  settings.TIME_ZONE))  # noqa
            datetime_data = {
                'datetime_year': aux_datetime.year,
                'datetime_month': aux_datetime.month,
                'datetime_day': aux_datetime.day,
                'datetime_hour': aux_datetime.hour,
                'datetime_minute': aux_datetime.minute,
                'datetime_second': aux_datetime.second,
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
            station=self.id, date__gte=from_date,
            date__lte=to_date).order_by('date').distinct()
        for record in data:
            historic_data.append({
                'date_obj':
                record.date,
                'date':
                record.date.strftime('%Y-%m-%d'),
                'temperature_mean':
                record.temperature_mean,
                'temperature_max':
                record.temperature_max,
                'temperature_min':
                record.temperature_min,
                'pressure_mean':
                record.pressure_mean,
                'pressure_max':
                record.pressure_max,
                'pressure_min':
                record.pressure_min,
                'relative_humidity_mean':
                record.relative_humidity_mean,
                'relative_humidity_max':
                record.relative_humidity_max,
                'relative_humidity_min':
                record.relative_humidity_min,
                'rain':
                record.rain
            })

        return historic_data

    def get_data_first_date(self):
        data = HistoricData.objects.filter(
            station=self.id).order_by('date').distinct()[0]
        return data.date


class Data(models.Model):
    """ Realtime data model class
    """
    station = models.ForeignKey(
        Station, verbose_name='stazione', on_delete=models.CASCADE)
    datetime = models.DateTimeField(
        'data e ora', auto_now=False, auto_now_add=False)
    temperature = models.DecimalField(
        'temperatura', max_digits=3, decimal_places=1, blank=True, null=True)
    temperature_max = models.DecimalField(
        'temperatura massima',
        max_digits=3,
        decimal_places=1,
        blank=True,
        null=True)
    temperature_max_time = models.TimeField(
        'ora temperatura massima', blank=True, null=True)
    temperature_min = models.DecimalField(
        'temperatura minima',
        max_digits=3,
        decimal_places=1,
        blank=True,
        null=True)
    temperature_min_time = models.TimeField(
        'ora temperatura minima', blank=True, null=True)
    relative_humidity = models.DecimalField(
        'umidità relativa',
        max_digits=4,
        decimal_places=1,
        blank=True,
        null=True)
    relative_humidity_max = models.DecimalField(
        'umidità relativa massima',
        max_digits=4,
        decimal_places=1,
        blank=True,
        null=True)
    relative_humidity_max_time = models.TimeField(
        'ora umidità relativa massima', blank=True, null=True)
    relative_humidity_min = models.DecimalField(
        'umidità relativa minima',
        max_digits=4,
        decimal_places=1,
        blank=True,
        null=True)
    relative_humidity_min_time = models.TimeField(
        'ora umidità relativa minima', blank=True, null=True)
    dewpoint = models.DecimalField(
        'dewpoint', max_digits=3, decimal_places=1, blank=True, null=True)
    dewpoint_max = models.DecimalField(
        'dewpoint massima',
        max_digits=3,
        decimal_places=1,
        blank=True,
        null=True)
    dewpoint_max_time = models.TimeField(
        'ora dewpoint massima', blank=True, null=True)
    dewpoint_min = models.DecimalField(
        'dewpoint minima',
        max_digits=3,
        decimal_places=1,
        blank=True,
        null=True)
    dewpoint_min_time = models.TimeField(
        'ora dewpoint minima', blank=True, null=True)
    pressure = models.DecimalField(
        'pressione', max_digits=5, decimal_places=1, blank=True, null=True)
    pressure_max = models.DecimalField(
        'pressione massima',
        max_digits=5,
        decimal_places=1,
        blank=True,
        null=True)
    pressure_max_time = models.TimeField(
        'ora pressione massima', blank=True, null=True)
    pressure_min = models.DecimalField(
        'pressione minima',
        max_digits=5,
        decimal_places=1,
        blank=True,
        null=True)
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
        'accumulo precipitazioni',
        max_digits=8,
        decimal_places=1,
        blank=True,
        null=True)
    rain_rate = models.DecimalField(
        'rateo precipitazioni',
        max_digits=8,
        decimal_places=1,
        blank=True,
        null=True)
    rain_rate_max = models.DecimalField(
        'rateo massimo precipitazioni',
        max_digits=8,
        decimal_places=1,
        blank=True,
        null=True)
    rain_rate_max_time = models.TimeField(
        'ora rateo massimo precipitazioni', blank=True, null=True)
    rain_month = models.DecimalField(
        'accumulo mensile precipitazioni',
        max_digits=8,
        decimal_places=1,
        blank=True,
        null=True)
    rain_year = models.DecimalField(
        'accumulo annuale precipitazioni',
        max_digits=8,
        decimal_places=1,
        blank=True,
        null=True)

    class Meta:
        verbose_name = 'Dati realtime'
        verbose_name_plural = 'Dati realtime'

    def __str__(self):
        return '%s - %s' % (self.station.name,
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
    station = models.ForeignKey(
        Station, verbose_name='stazione', on_delete=models.CASCADE)
    date = models.DateField('data', auto_now=False, auto_now_add=False)
    temperature_max = models.DecimalField(
        'temperatura massima',
        max_digits=3,
        decimal_places=1,
        blank=True,
        null=True)
    temperature_min = models.DecimalField(
        'temperatura minima',
        max_digits=3,
        decimal_places=1,
        blank=True,
        null=True)
    temperature_mean = models.DecimalField(
        'temperatura media',
        max_digits=3,
        decimal_places=1,
        blank=True,
        null=True)
    relative_humidity_max = models.DecimalField(
        'umidità relativa massima',
        max_digits=4,
        decimal_places=1,
        blank=True,
        null=True)
    relative_humidity_min = models.DecimalField(
        'umidità relativa minima',
        max_digits=4,
        decimal_places=1,
        blank=True,
        null=True)
    relative_humidity_mean = models.DecimalField(
        'umidità relativa media',
        max_digits=4,
        decimal_places=1,
        blank=True,
        null=True)
    pressure_max = models.DecimalField(
        'pressione massima',
        max_digits=5,
        decimal_places=1,
        blank=True,
        null=True)
    pressure_min = models.DecimalField(
        'pressione minima',
        max_digits=5,
        decimal_places=1,
        blank=True,
        null=True)
    pressure_mean = models.DecimalField(
        'pressione media',
        max_digits=5,
        decimal_places=1,
        blank=True,
        null=True)
    rain = models.DecimalField(
        'accumulo precipitazioni',
        max_digits=8,
        decimal_places=1,
        blank=True,
        null=True)

    class Meta:
        verbose_name = 'Dati storici'
        verbose_name_plural = 'Dati storici'

    def __str__(self):
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
    web_site_url = models.URLField(
        'URL sito web', max_length=255, blank=True, null=True)
    webcam_url = models.URLField(
        'Webcam URL', max_length=255, blank=True, null=True)
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
    installation_type = models.CharField(
        'tipo di installazione', max_length=255)
    installation_position = models.CharField('ubicazione', max_length=255)
    elevation_ground = models.DecimalField(
        'altezza dal suolo (m)', max_digits=5, decimal_places=2)
    data_url = models.URLField('URL dati realtime', blank=True, null=True)
    image = models.ImageField(upload_to=set_net_request_image_folder)

    class Meta:
        verbose_name = 'Richiesta ingresso nella rete'
        verbose_name_plural = 'Richieste ingresso nella rete'

    def __str__(self):
        return '%s %s - %s' % (self.firstname, self.lastname, self.city)


class RadarSnapshot(models.Model):
    datetime = models.DateTimeField(
        'data e ora', auto_now=False, auto_now_add=False)  # noqa
    filename = models.CharField('nome file', max_length=128)
    save_datetime = models.DateTimeField('salvataggio', auto_now=True)

    class Meta:
        verbose_name = "Immagine radar"
        verbose_name_plural = "Immagini radar"

    def __str__(self):
        return self.filename


class RadarColorConversion(models.Model):
    original_color = RGBColorField(verbose_name='colore iniziale')
    converted_color = RGBColorField(verbose_name='colore finale')
    tolerance = models.IntegerField('tolleranza')

    class Meta:
        verbose_name = "Conversione colore radar"
        verbose_name_plural = "Conversioni colori radar"

    def __str__(self):
        return '%s - %s' % (self.original_color, str(self.converted_color))


class RadarConvertParams(models.Model):
    param_name = models.CharField('nome parametro', max_length=50)
    param_value = models.CharField('valore parametro', max_length=50)

    class Meta:
        verbose_name = "Parametri comando convert"
        verbose_name_plural = "Parametri comando convert"

    def __str__(self):
        return '%s' % self.param_name


class StationForecast(models.Model):
    PERIOD_NIGHT = 0
    PERIOD_MORNING = 1
    PERDIOD_AFTERNOON = 2
    PERIOD_EVENING = 3
    PERIOD_CHOICES = (
        (PERIOD_NIGHT, '00:00 06:00'),
        (PERIOD_MORNING, '06:00 12:00'),
        (PERDIOD_AFTERNOON, '12:00 18:00'),
        (PERIOD_EVENING, '18:00 24:00'),
    )
    last_edit = models.DateTimeField('ultima modifica')
    station = models.ForeignKey(
        Station, verbose_name='stazione', on_delete=models.CASCADE)
    date = models.DateField('data')
    period = models.IntegerField('periodo', choices=PERIOD_CHOICES)
    icon = models.CharField('icona', max_length=255)
    text = models.CharField('testo', max_length=50)
    data = models.TextField('json data')

    class Meta:
        verbose_name = "Previsione"
        verbose_name_plural = "Previsioni"

    def __str__(self):
        return '%s' % self.icon


class AirQualityStation(models.Model):
    # range in seconds for data to be considered live
    RT_RANGE_SECONDS = 60 * 70
    """ Station model
    """
    name = models.CharField('nome', max_length=128)
    slug = models.SlugField('slug', max_length=128)
    short_name = models.CharField(
        'nome abbreviato', max_length=64, null=True, blank=True)
    station = models.ForeignKey(Station, verbose_name='stazione meteo', on_delete=models.SET_NULL, related_name='airquality_stations', blank=True, null=True)
    description = RichTextUploadingField('descrizione')
    data_url = models.URLField('URL dati')
    nation = models.ForeignKey(
        Nation,
        verbose_name='nazione',
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    region = models.ForeignKey(
        Region,
        verbose_name='regione',
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    province = models.ForeignKey(
        Province,
        verbose_name='provincia',
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    address = models.CharField(
        'indirizzo', max_length=255, blank=True, null=True)
    city = models.CharField(
        'città/comune', max_length=255, blank=True, null=True)
    cap = models.CharField('cap', max_length=10, blank=True, null=True)
    lat = models.CharField('latitudine', max_length=255)
    lng = models.CharField('longitudine', max_length=255)
    elevation = models.IntegerField('altitudine', blank=True, null=True)

    active = models.BooleanField('attiva', default=True)

    objects = AirQualityStationManager()

    class Meta:
        verbose_name = 'stazione aria'
        verbose_name_plural = 'stazioni aria'
        ordering = ('name', )

    def __str__(self):
        return '%s' % self.name

    def now(self):
        """ Returns the current datetime, for debug and dev purposes
        """
        return timezone.now()
        # datetime_obj = datetime.datetime(2015, 03, 11, 10, 40, 00)
        # return timezone.make_aware(datetime_obj,
        #                           timezone.get_current_timezone())

    def get_realtime_data(self):
        """ Last measured data, if inside the AirQualityStation.RT_RANGE_SECONDS range
            http://stackoverflow.com/questions/21918802/problems-filtering-django-datetime-field-by-month-and-day
        """
        date = self.now()
        try:
            data = AirQualityData.objects.filter(
                station=self.id,
                datetime__year=date.year,
                datetime__month=date.month,
                datetime__day=date.day).order_by('-id').first()
            time_difference = self.now() - data.datetime
            if (time_difference.total_seconds() > AirQualityStation.RT_RANGE_SECONDS):
                return None

            return data
        except:
            return None


class AirQualityData(models.Model):
    station = models.ForeignKey(AirQualityStation, verbose_name='stazione', on_delete=models.CASCADE, related_name='data', )
    datetime = models.DateTimeField('data e ora', auto_now=False, auto_now_add=False)
    air_quality_index = models.DecimalField(
        'indice qualità dell\'aria', max_digits=4, decimal_places=1)
    pm1 = models.DecimalField('pm 1', max_digits=8, decimal_places=1)
    pm1_max = models.DecimalField('pm 1 massimo', max_digits=8, decimal_places=1)
    pm1_max_time = models.TimeField(
        'ora pm 1 massimo', blank=True, null=True)
    pm1_min = models.DecimalField('pm 1 minimo', max_digits=8, decimal_places=1)
    pm1_min_time = models.TimeField(
        'ora pm 1 massimo', blank=True, null=True)
    pm25 = models.DecimalField('pm 2.5', max_digits=8, decimal_places=1)
    pm25_max = models.DecimalField('pm 2.5 massimo', max_digits=8, decimal_places=1)
    pm25_max_time = models.TimeField(
        'ora pm 2.5 massimo', blank=True, null=True)
    pm25_min = models.DecimalField('pm 2.5 minimo', max_digits=8, decimal_places=1)
    pm25_min_time = models.TimeField(
        'ora pm 2.5 minimo', blank=True, null=True)
    pm10 = models.DecimalField('pm 10', max_digits=8, decimal_places=1)
    pm10_max = models.DecimalField('pm 10 massimo', max_digits=8, decimal_places=1)
    pm10_max_time = models.TimeField(
        'ora pm 10 massimo', blank=True, null=True)
    pm10_min = models.DecimalField('pm 10 minimo', max_digits=8, decimal_places=1)
    pm10_min_time = models.TimeField(
        'ora pm 10 minimo', blank=True, null=True)

    class Meta:
        verbose_name = 'Dati qualità dell\'aria'
        verbose_name_plural = 'Dati qualità dell\'aria'

    def __str__(self):
        return '%s - %s' % (self.station.name,
                            str(self.datetime) if self.datetime else '')


class HistoricAirQualityData(models.Model):
    station = models.ForeignKey(AirQualityStation, verbose_name='stazione', on_delete=models.CASCADE, related_name='historic_data', )
    date = models.DateField('data', auto_now=False, auto_now_add=False)
    air_quality_index_max = models.DecimalField(
        'indice qualità dell\'aria massimo', max_digits=4, decimal_places=1)
    air_quality_index_min = models.DecimalField(
        'indice qualità dell\'aria minimo', max_digits=4, decimal_places=1)
    air_quality_index_mean = models.DecimalField(
        'indice qualità dell\'aria medio', max_digits=4, decimal_places=1)
    pm1_max = models.DecimalField('pm 1 massimo', max_digits=8, decimal_places=1)
    pm1_min = models.DecimalField('pm 1 minimo', max_digits=8, decimal_places=1)
    pm1_mean = models.DecimalField('pm 1 minimo', max_digits=8, decimal_places=1)
    pm25_max = models.DecimalField('pm 2.5 massimo', max_digits=8, decimal_places=1)
    pm25_min = models.DecimalField('pm 2.5 minimo', max_digits=8, decimal_places=1)
    pm25_mean = models.DecimalField('pm 2.5 minimo', max_digits=8, decimal_places=1)
    pm10_max = models.DecimalField('pm 10 massimo', max_digits=8, decimal_places=1)
    pm10_min = models.DecimalField('pm 10 minimo', max_digits=8, decimal_places=1)
    pm10_mean = models.DecimalField('pm 10 minimo', max_digits=8, decimal_places=1)

    class Meta:
        verbose_name = 'Dati storici qualità dell\'aria'
        verbose_name_plural = 'Dati storici qualità dell\'aria'

    def __str__(self):
        return '%s - %s' % (self.station, self.date)
