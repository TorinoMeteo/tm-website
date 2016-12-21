from __future__ import absolute_import

import datetime

from django.db.models import Max, Min, Avg

from core.celery import app
from celery.utils.log import get_task_logger

from .models.stations import Station, Data, HistoricData
from .fetch.shortcuts import fetch_data

logger = get_task_logger(__name__)


def patch_max(station, datetime, variable):
    max = Data.objects.filter(
        station=station,
        datetime__gte=datetime.date()
    ).order_by('-%s' % variable).first()
    if max:
        return (getattr(max, variable), getattr(max, 'datetime').time())
    return (None, None)


def patch_min(station, datetime, variable):
    """ Retrieves and patches missing max and min from prev measures
    """
    min = Data.objects.filter(
        station=station,
        datetime__gte=datetime.date()
    ).order_by('%s' % variable).first()
    if min:
        return (getattr(min, variable), getattr(min, 'datetime').time())
    return (None, None)


def patch_wind_max(station, datetime):
    """ Retrieves and patches missing max wind
    """
    max = Data.objects.filter(
        station=station,
        datetime__gte=datetime.date()
    ).order_by('-wind_strength').first()
    if max:
        return (max.wind_strength, max.wind_dir, max.datetime.time())
    return (None, None, None)


def adjust_data(station, data):
    """ Adjusts data to be eaten by model creator
    """
    # add station
    data['station'] = station
    # remove single date and time
    data.pop('date', None)
    data.pop('time', None)
    # patch max and min
    for var in ['temperature', 'pressure', 'dewpoint', 'relative_humidity', 'rain_rate']: # noqa
        if ('%s_max' % var) not in data or data['%s_max' % var] is None:
            (data['%s_max' % var], data['%s_max_time' % var]) = patch_max(
                station, data['datetime'], var
            )
        if var != 'rain_rate':  # rain rate has no min
            if ('%s_min' % var) not in data or data['%s_min' % var] is None:
                (data['%s_min' % var], data['%s_min_time' % var]) = patch_min(
                    station, data['datetime'], var
                )
    if 'wind_strength_max' not in data or data['wind_strength_max'] is None:
        (data['wind_strength_max'], data['wind_dir_max'], data['wind_max_time']) = patch_wind_max( # noqa
            station, data['datetime']
        )
    return data


def data_exists(station, datetime):
    """ Checks if datetime data was already saved
    """
    count = Data.objects.filter(
        station=station,
        datetime=datetime
    ).count()
    return True if count else False


@app.task
def fetch_realtime_data():
    """ Fetches all realtime data from external urls
        and populates the db
    """
    logger.info('BEGIN -- running task: fetch_realtime_data')

    for station in Station.objects.active():
        try:
            data = fetch_data(
                station.data_url,
                station.data_format.name,
                time_format=station.data_time_format.split(','),
                date_format=station.data_date_format.split(','),
            )
            if not data_exists(station, data['datetime']):
                new_data = Data(**adjust_data(station, data))
                new_data.save()
                logger.info('station %s fetch successfull' % (station.name))

        except Exception, e:
            logger.warn('station %s fetch failed: %s' % (station.name, str(e))) # noqa

    logger.info('END -- running task: fetch_realtime_data')
    return True


@app.task
def store_historic_data():
    """ Stores max min and avg values for yesterday
    """
    logger.info('BEGIN -- running task: store_historic_data')
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)

    for station in Station.objects.active():
        try:
            # @CHECKME maybe data should be filtered date > yesterday 00:06:00
            data = Data.objects.filter(
                station=station,
                datetime__year=yesterday.year,
                datetime__month=yesterday.month,
                datetime__day=yesterday.day,
            )
            # temperature
            max_temp = data.aggregate(Max('temperature_max'))
            min_temp = data.aggregate(Min('temperature_min'))
            avg_temp = data.aggregate(Avg('temperature'))
            # relative humidity
            max_rh = data.aggregate(Max('relative_humidity_max'))
            min_rh = data.aggregate(Min('relative_humidity_min'))
            avg_rh = data.aggregate(Avg('relative_humidity'))
            # temperature
            max_press = data.aggregate(Max('pressure_max'))
            min_press = data.aggregate(Min('pressure_min'))
            avg_press = data.aggregate(Avg('pressure'))
            # rain
            max_rain = data.aggregate(Max('rain'))

            history = HistoricData(
                station=station,
                date=yesterday.date(),
                temperature_max=max_temp['temperature_max__max'],
                temperature_min=min_temp['temperature_min__min'],
                temperature_mean=avg_temp['temperature__avg'],
                relative_humidity_max=max_rh['relative_humidity_max__max'],
                relative_humidity_min=min_rh['relative_humidity_min__min'],
                relative_humidity_mean=avg_rh['relative_humidity__avg'],
                pressure_max=max_press['pressure_max__max'],
                pressure_min=min_press['pressure_min__min'],
                pressure_mean=avg_press['pressure__avg'],
                rain=max_rain['rain__max'],
            )
            history.save()
            logger.info('station %s history save successfull' % (station.name))
        except Exception, e:
            logger.warn('station %s history save failed: %s' % (station.name, str(e))) # noqa

    logger.info('END -- running task: store_historic_data')


@app.task
def clean_realtime_data():
    """ Deletes data older than 1 week
    """
    logger.info('BEGIN -- running task: clean_realtime_data')
    date = datetime.datetime.now() - datetime.timedelta(days=7)
    Data.objects.filter(datetime__lte=date).delete()
    logger.info('delete realtime data older than 1 week successfull')
    logger.info('END -- running task: clean_realtime_data')
