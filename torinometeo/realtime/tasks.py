from __future__ import absolute_import

import datetime
import json
import os
import shutil
from urllib.request import urlopen, Request
import dateutil.parser

import pytz
import requests
from bs4 import BeautifulSoup
from celery.utils.log import get_task_logger
from constance import config
from django.conf import settings
from django.db.models import Avg, Max, Min
from requests.exceptions import HTTPError
from stem import Signal
from stem.control import Controller

from core.celery import app

from .fetch.shortcuts import fetch_data
from .models.stations import (AirQualityData, AirQualityStation, Data,
                              HistoricData, RadarColorConversion,
                              RadarConvertParams, RadarSnapshot, Station,
                              StationForecast)

logger = get_task_logger(__name__)


def patch_max(station, datetime, variable):
    max = Data.objects.filter(station=station,
                              datetime__gte=datetime.date()).order_by(
                                  '-%s' % variable).first()
    if max:
        return (getattr(max, variable), getattr(max, 'datetime').time())
    return (None, None)


def patch_min(station, datetime, variable):
    """ Retrieves and patches missing max and min from prev measures
    """
    min = Data.objects.filter(station=station,
                              datetime__gte=datetime.date()).order_by(
                                  '%s' % variable).first()
    if min:
        return (getattr(min, variable), getattr(min, 'datetime').time())
    return (None, None)


def patch_wind_max(station, datetime):
    """ Retrieves and patches missing max wind
    """
    max = Data.objects.filter(
        station=station,
        datetime__gte=datetime.date()).order_by('-wind_strength').first()
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
    for var in [
            'temperature', 'pressure', 'dewpoint', 'relative_humidity',
            'rain_rate'
    ]:  # noqa
        if ('%s_max' % var) not in data or data['%s_max' % var] is None:
            (data['%s_max' % var],
             data['%s_max_time' % var]) = patch_max(station, data['datetime'],
                                                    var)
        if var != 'rain_rate':  # rain rate has no min
            if ('%s_min' % var) not in data or data['%s_min' % var] is None:
                (data['%s_min' % var], data['%s_min_time' % var]) = patch_min(
                    station, data['datetime'], var)
    if 'wind_strength_max' not in data or data['wind_strength_max'] is None:
        (data['wind_strength_max'], data['wind_dir_max'],
         data['wind_max_time']) = patch_wind_max(  # noqa
             station, data['datetime'])
    return data


def data_exists(station, datetime):
    """ Checks if datetime data was already saved
    """
    count = Data.objects.filter(station=station, datetime=datetime).count()
    return True if count else False


def airqualitydata_exists(station, datetime):
    """ Checks if datetime airquality data was already saved
    """
    count = AirQualityData.objects.filter(station=station, datetime=datetime).count()
    return True if count else False


@app.task
def fetch_realtime_data():
    """ Fetches all realtime data from external urls
        and populates the db
    """
    logger.info('BEGIN -- running task: fetch_realtime_data')

    for station in Station.objects.active():
        try:
            url = station.data_url
            # GreenPlanet needs some more work, is a private :D API
            if station.data_format.name == 'greenplanet':
                url = url + "&dtfrom=%s&dtto=%s" % (
                    datetime.datetime.now().strftime('%Y-%m-%d'),
                    datetime.datetime.now().strftime('%Y-%m-%d'),
                )
            data = fetch_data(
                url,
                station.data_format.name,
                time_format=station.data_time_format.split(',')
                if station.data_time_format else None,
                date_format=station.data_date_format.split(',')
                if station.data_date_format else None,
                headers={ "Authorization": station.data_token } if station.data_token else {},
                station=station,
            )
            if not data_exists(station, data['datetime']):
                new_data = Data(**adjust_data(station, data))
                new_data.save()
                logger.info('station %s fetch successfull' % (station.name))

        except Exception as e:
            logger.warn('station %s fetch failed: %s' %
                        (station.name, str(e)))  # noqa

    logger.info('END -- running task: fetch_realtime_data')
    return True


@app.task
def fetch_airquality_data():
    """ Fetches all airquality data from external urls
        and populates the db
    """
    logger.info('BEGIN -- running task: fetch_airquality_data')

    for station in AirQualityStation.objects.active():
        try:
            data = fetch_data(
                station.data_url,
                'airquality',
            )
            if not airqualitydata_exists(station, data['datetime']):
                new_data = AirQualityData(station=station, **data)
                new_data.save()
                logger.info('station %s fetch successfull' % (station.name))

        except Exception as e:
            logger.warn('station %s fetch failed: %s' %
                        (station.name, str(e)))  # noqa

    logger.info('END -- running task: fetch_airquality_data')
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
        except Exception as e:
            logger.warn('station %s history save failed: %s' %
                        (station.name, str(e)))  # noqa

    logger.info('END -- running task: store_historic_data')


@app.task
def store_air_quality_historic_data():
    """ Stores max min and avg values for yesterday
    """
    logger.info('BEGIN -- running task: store_air_quality_historic_data')
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)

    for station in AirQualityStation.objects.active():
        try:
            # @CHECKME maybe data should be filtered date > yesterday 00:06:00
            data = AirQualityData.objects.filter(
                station=station,
                datetime__year=yesterday.year,
                datetime__month=yesterday.month,
                datetime__day=yesterday.day,
            )

            # air quality index
            max_air_quality_index = data.aggregate(Max('air_quality_index_max'))
            min_air_quality_index = data.aggregate(Min('air_quality_index_min'))
            avg_air_quality_index = data.aggregate(Avg('air_quality_index'))
            # pm1
            max_pm1 = data.aggregate(Max('pm1_max'))
            min_pm1 = data.aggregate(Min('pm1_min'))
            avg_pm1 = data.aggregate(Avg('pm1'))
            # pm2.5
            max_pm25 = data.aggregate(Max('pm25_max'))
            min_pm25 = data.aggregate(Min('pm25_min'))
            avg_pm25 = data.aggregate(Avg('pm25'))
            # temperature
            max_pm10 = data.aggregate(Max('pm10_max'))
            min_pm10 = data.aggregate(Min('pm10_min'))
            avg_pm10 = data.aggregate(Avg('pm10'))

            history = HistoricAirQualityData(
                station=station,
                date=yesterday.date(),
                air_quality_index_max=max_air_quality_index['air_quality_index_max__max'],
                air_quality_index_min=min_air_quality_index['air_quality_index_min__min'],
                air_quality_index_mean=avg_air_quality_index['air_quality_index_min__avg'],
                pm1_max=max_pm1['pm1_max__max'],
                pm1_min=min_pm1['pm1_min__min'],
                pm1_mean=avg_pm1['pm1__avg'],
                pm25_max=max_pm25['pm25_max__max'],
                pm25_min=min_pm25['pm25_min__min'],
                pm25_mean=avg_pm25['pm25__avg'],
                pm10_max=max_pm10['pm10_max__max'],
                pm10_min=min_pm10['pm10_min__min'],
                pm10_mean=avg_pm10['pm10__avg'],
            )
            history.save()
            logger.info('station %s history save successfull' % (station.name))
        except Exception as e:
            logger.warn('station %s history save failed: %s' %
                        (station.name, str(e)))  # noqa

    logger.info('END -- running task: store_air_quality_historic_data')


@app.task
def clean_realtime_data():
    """ Deletes data older than 1 week
    """
    logger.info('BEGIN -- running task: clean_realtime_data')
    date = datetime.datetime.now() - datetime.timedelta(days=7)
    Data.objects.filter(datetime__lte=date).delete()
    logger.info('delete realtime data older than 1 week successfull')
    logger.info('END -- running task: clean_realtime_data')


@app.task
def clean_air_quality_data():
    """ Deletes data older than 1 week
    """
    logger.info('BEGIN -- running task: clean_air_quality_data')
    date = datetime.datetime.now() - datetime.timedelta(days=7)
    AirQualityData.objects.filter(datetime__lte=date).delete()
    logger.info('delete air quality data older than 1 week successfull')
    logger.info('END -- running task: clean_air_quality_data')

# radar
# Get Radar Image Based On Input timestamp if availale
def fetch_radar_image(dt, src):
    remainder_dt = int(dt.minute) % 10
    next_dt = dt + datetime.timedelta(minutes=10) - datetime.timedelta(
        minutes=remainder_dt)  # noqa
    base_url = config.RADAR_BASE_URL
    remote_filename = 'VRAG05.CCSK_%s' % next_dt.astimezone(pytz.utc).strftime(
        "%Y%m%d_%H%M")  # noqa
    local_filename = '%s.png' % next_dt.astimezone(pytz.utc).strftime(
        "%Y%m%d%H%M")  # noqa
    local_path = os.path.join(src, local_filename)
    image_dt = next_dt
    try:
        session = requests.session()
        # Tor uses the 9050 port as the default socks port
        session.proxies = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050'
        }
        ip = get_ip(session)
        #r = session.get('http://media.meteonews.net/radar/chComMET_800x618_c2/%s.png' % remote_filename, stream=True) # noqa
        headers = {
            'Host':
            'www.meteosvizzera.admin.ch',
            'Referer':
            'http://www.meteosvizzera.admin.ch/home.html?tab=rain',
            'USer-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'  # noqa
        }
        r = session.get(base_url + remote_filename + '.png',
                        headers=headers,
                        stream=True)  # noqa
        r.raise_for_status()
        with open(local_path, 'wb') as out_file:
            shutil.copyfileobj(r.raw, out_file)
        del r
        return (ip, local_filename, image_dt)
    except HTTPError:
        logger.error('Could not download ' + base_url + remote_filename +
                     '.png')
        return False
    except Exception as e:
        logger.error(e)
        return False


# Execute external script to change image color based on Color Replacement List
def change_colors(img_path, conversions):
    for conversion in conversions:
        cmd = "convert " + img_path + " -fuzz " + str(
            conversion[2]) + "% -fill \"" + str(
                conversion[1]) + "\" -opaque \"" + str(
                    conversion[0]) + "\" " + img_path  # noqa
        logger.info('Executing imagemagick command: %s' % cmd)
        os.system(cmd)
        params = [
            '-%s %s' % (p.param_name, p.param_value)
            for p in RadarConvertParams.objects.all()
        ]  # noqa
        cmd = "convert %s %s %s" % (img_path, ' '.join(params), img_path)
        logger.info('Executing imagemagick command: %s' % cmd)
        os.system(cmd)


# Reset Tor circuit to get ne ip address
def reset_tor_circuit():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate('ri3313co')
        controller.signal(Signal.NEWNYM)
    return "Tor Circuit Reset Done"


# Get Current Ip - Just for debug
def get_ip(session):
    ip = session.get('https://api.ipify.org').text
    return ip


# Fetch Radar Image
def fetch_radar(dt, colors, src, dst):
    try:
        logger.info(reset_tor_circuit())
    except:
        logger.error('cannot reset tor')
    image_data = fetch_radar_image(dt, src)
    if (image_data):
        (ip, filename, datetime) = image_data
        if filename:
            logger.info('%s downloaded with IP %s' % (filename, ip))
            change_colors(os.path.join(src, filename), colors)  # noqa
            try:
                shutil.move(os.path.join(src, filename),
                            os.path.join(dst, filename))  # noqa
            except Exception as e:
                logger.error('cannot move the image %s' % e)
                return False
        else:
            logger.error('Image download Error with IP %s' % ip)
            return False
        try:
            os.remove(os.path.join(src, filename))
        except:
            pass

        return {'filename': filename, 'datetime': datetime, 'ip': ip}
    else:
        return False


@app.task
def fetch_radar_images():
    logger.info('BEGIN -- running task: fetch_radar_images')
    dt = datetime.datetime(2017, 7, 5, 6, 0, 0)
    try:
        last_radar_image = RadarSnapshot.objects.last()
        if last_radar_image:
            dt = last_radar_image.datetime
    except:
        pass
    colors = [(c.original_color, c.converted_color, c.tolerance)
              for c in RadarColorConversion.objects.all()]  # noqa

    src = '/tmp/'
    if settings.DEBUG:
        dst = '/home/abidibo/Junk/'
    else:
        dst = '/var/www/radar/images/'

    result = fetch_radar(dt, colors, src, dst)
    if not result:
        result = fetch_radar((dt + datetime.timedelta(minutes=10)), colors,
                             src, dst)
    if result:
        snapshot = RadarSnapshot(datetime=result.get('datetime'),
                                 filename=result.get('filename'))
        snapshot.save()
    logger.info('END -- running task: fetch_radar_images')
    return result


@app.task
def fetch_weather_forecast():
    logger.info('BEGIN -- running task: fetch_weather_forecast')
    for station in Station.objects.active():
        try:
            url = "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=%s&lon=%s" % (station.lat, station.lng)
            hdr = { 'User-Agent' : 'torinometeo.org info@torinometeo.org' }

            req = Request(url, headers=hdr)
            response = urlopen(req).read()
            json_response = json.loads(response)
            for obj in json_response.get('properties', {}).get('timeseries', []):
                date = None
                period = None
                icon = None

                time = obj.get('time', None)
                time_obj = dateutil.parser.parse(time)

                if time_obj.hour == 0 and time_obj.minute == 0 and time_obj.second == 0:
                    data = obj.get('data', {}).get('next_6_hours', {})
                    date = time_obj.date()
                    period = 0
                    icon = data.get('summary', {}).get('symbol_code', None)
                elif time_obj.hour == 6 and time_obj.minute == 0 and time_obj.second == 0:
                    data = obj.get('data', {}).get('next_6_hours', {})
                    date = time_obj.date()
                    period = 1
                    icon = data.get('summary', {}).get('symbol_code', None)
                elif time_obj.hour == 12 and time_obj.minute == 0 and time_obj.second == 0:
                    data = obj.get('data', {}).get('next_6_hours', {})
                    date = time_obj.date()
                    period = 2
                    icon = data.get('summary', {}).get('symbol_code', None)
                elif time_obj.hour == 18 and time_obj.minute == 0 and time_obj.second == 0:
                    data = obj.get('data', {}).get('next_6_hours', {})
                    date = time_obj.date()
                    period = 3
                    icon = data.get('summary', {}).get('symbol_code', None)

                if date:
                    try:
                        forecast = StationForecast.objects.get(
                            station=station,
                            date=date,
                            period=period,
                        )
                    except:
                        forecast = StationForecast(
                            station=station,
                            date=date,
                            period=period,
                        )
                    forecast.last_edit = dateutil.parser.parse(json_response.get('properties').get('meta').get('updated_at'))
                    forecast.icon = icon
                    forecast.text = ''
                    forecast.data = ''
                    forecast.save()
        except:
            pass
    logger.info('END -- running task: fetch_weather_forecast')


@app.task
def clean_weather_forecast():
    """ Deletes data older than 2 days
    """
    logger.info('BEGIN -- running task: clean_weather_forecast')
    date = datetime.datetime.now() - datetime.timedelta(days=2)
    StationForecast.objects.filter(date__lte=date).delete()
    logger.info('delete station forecast older than 2 days successfull')
    logger.info('END -- running task: clean_weather_forecast')
