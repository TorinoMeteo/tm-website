import json
import os
import re
import dateutil.parser
import pytz

from realtime.models.stations import Data

from ..labels import DATA_LABELS as DL
from .abstract import Parser


class GreenplanetParser(Parser):
    def parse(self, content, **kwargs):
        station = kwargs.get('station')
        json_data = json.loads(content)
        data_list = json_data.get('list')
        or_data = None
        for d in data_list:
            if d.get('TemperaturaAriaMedia') != "":
                or_data = d

        if or_data is not None:
            date = dateutil.parser.parse(or_data.get('Data'))
            date_aware = date.replace(tzinfo=pytz.timezone('Europe/London'))

            max_temp = float(or_data.get('TemperaturaAriaMax'))
            max_temp_time = date_aware.time()
            max_temp_prev = Data.objects.filter(station=station, datetime__date=date_aware.date()).order_by('-temperature_max').first()
            if max_temp_prev is not None:
                if max_temp_prev.temperature_max > max_temp:
                    max_temp = max_temp_prev.temperature_max
                    max_temp_time = max_temp_prev.temperature_max_time

            min_temp = float(or_data.get('TemperaturaAriaMin'))
            min_temp_time = date_aware.time()
            min_temp_prev = Data.objects.filter(station=station, datetime__date=date_aware.date()).order_by('-temperature_min').first()
            if min_temp_prev is not None:
                if min_temp_prev.temperature_min < min_temp:
                    min_temp = min_temp_prev.temperature_min
                    min_temp_time = min_temp_prev.temperature_min_time

            max_relative_humidity = float(or_data.get('UmiditaRelativaMax'))
            max_relative_humidity_time = date_aware.time()
            max_relative_humidity_prev = Data.objects.filter(station=station, datetime__date=date_aware.date()).order_by('-relative_humidity_max').first()
            if max_relative_humidity_prev is not None:
                if max_relative_humidity_prev.relative_humidity_max > max_relative_humidity:
                    max_relative_humidity = max_relative_humidity_prev.relative_humidity_max
                    max_relative_humidity_time = max_relative_humidity_prev.relative_humidity_max_time

            min_relative_humidity = float(or_data.get('UmiditaRelativaMin'))
            min_relative_humidity_time = date_aware.time()
            min_relative_humidity_prev = Data.objects.filter(station=station, datetime__date=date_aware.date()).order_by('-relative_humidity_min').first()
            if min_relative_humidity_prev is not None:
                if min_relative_humidity_prev.relative_humidity_min < min_relative_humidity:
                    min_relative_humidity = min_relative_humidity_prev.relative_humidity_min
                    min_relative_humidity_time = min_relative_humidity_prev.relative_humidity_min_time

            max_wind = float(or_data.get('VelocitaVento2mMax'))
            max_wind_time = date_aware.time()
            max_wind_prev = Data.objects.filter(station=station, datetime__date=date_aware.date()).order_by('-wind_strength_max').first()
            if max_wind_prev is not None:
                if max_wind_prev.wind_strength_max > max_wind:
                    max_wind = max_wind_prev.wind_strength_max
                    max_wind_time = max_wind_prev.wind_max_time

            data = {
                'time': date.time(),
                'date': date.date(),
                'temperature': float(or_data.get('TemperaturaAriaMedia')),
                'temperature_max': max_temp,
                'temperature_max_time': max_temp_time,
                'temperature_min': min_temp,
                'temperature_min_time': min_temp_time,
                'relative_humidity': float(or_data.get('UmiditaRelativaMedia')),
                'relative_humidity_max': max_relative_humidity,
                'relative_humidity_max_time': max_relative_humidity_time,
                'relative_humidity_min': min_relative_humidity,
                'relative_humidity_min_time': min_relative_humidity_time,
                'dewpoint': None,
                'dewpoint_max': None,
                'dewpoint_max_time': None,
                'dewpoint_min': None,
                'dewpoint_min_time': None,
                'pressure': None,
                'pressure_max': None,
                'pressure_max_time': None,
                'pressure_min': None,
                'pressure_min_time': None,
                'wind_strength': float(or_data.get('VelocitaVento2mMedia')),
                'wind_dir': None,
                'wind_strength_max': max_wind,
                'wind_dir_max': None,
                'wind_max_time': max_wind_time,
                'rain': None,
                'rain_rate': float(or_data.get('Pioggia')),
                'rain_rate_max': None,
                'rain_rate_max_time': None,
                'rain_month': None,
                'rain_year': None
            }

            return data
