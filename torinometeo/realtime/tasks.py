from __future__ import absolute_import

from core.celery import app
from celery.utils.log import get_task_logger

from .models.stations import Station, Data
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


def adjust_data(station, data):
    """ Adjusts data to be eaten by model creator
    """
    # add station
    data['station'] = station
    # remove single date and time
    data.pop('date', None)
    data.pop('time', None)
    # patch max and min
    for var in ['temperature', 'pressure', 'dewpoint', 'relative_humidity']:
        if ('%s_max' % var) not in data or data['%s_max' % var] is None:
            (data['%s_max' % var], data['%s_max_time' % var]) = patch_max(
                station, data['datetime'], var
            )
        if ('%s_min' % var) not in data or data['%s_min' % var] is None:
            (data['%s_min' % var], data['%s_min_time' % var]) = patch_min(
                station, data['datetime'], var
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


@app.task # noqa
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
