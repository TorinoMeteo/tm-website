import json
import os
import re

import dateutil.parser

from ..labels import DATA_LABELS as DL
from .abstract import Parser


class Weatherlink2Parser(Parser):

    # line num: (label, clean)
    data_map = {
        'temp_c': (DL['TEMP'], 'temp'),
        'davis_current_observation.temp_day_high_f': (DL['TEMP_MAX'], 'tempf'),
        'davis_current_observation.temp_day_high_time': (DL['TEMP_MAX_TIME'], 'time'),
        'davis_current_observation.temp_day_low_f': (DL['TEMP_MIN'], 'tempf'),
        'davis_current_observation.temp_day_low_time': (DL['TEMP_MIN_TIME'], 'time'),
        'relative_humidity': (DL['HUMIDITY'], 'humidity'),
        'davis_current_observation.relative_humidity_day_high': (DL['HUMIDITY_MAX'], 'humidity'),
        'davis_current_observation.relative_humidity_day_high_time': (DL['HUMIDITY_MAX_TIME'], 'time'),
        'davis_current_observation.relative_humidity_day_low': (DL['HUMIDITY_MIN'], 'humidity'),
        'davis_current_observation.relative_humidity_day_low_time': (DL['HUMIDITY_MIN_TIME'], 'time'),
        'dewpoint_c': (DL['DEW'], 'dew'),
        'davis_current_observation.dewpoint_day_high_f': (DL['DEW_MAX'], 'dewf'),
        'davis_current_observation.dewpoint_day_high_time': (DL['DEW_MAX_TIME'], 'time'),
        'davis_current_observation.dewpoint_day_low_f': (DL['DEW_MIN'], 'dewf'),
        'davis_current_observation.dewpoint_day_low_time': (DL['DEW_MIN_TIME'], 'time'),
        'pressure_mb': (DL['PRESSURE'], 'pressure'),
        'davis_current_observation.pressure_day_high_in': (DL['PRESSURE_MAX'], 'pressurein'),
        'davis_current_observation.pressure_day_high_time': (DL['PRESSURE_MAX_TIME'], 'time'),
        'davis_current_observation.pressure_day_low_in': (DL['PRESSURE_MIN'], 'pressurein'),
        'davis_current_observation.pressure_day_low_time': (DL['PRESSURE_MIN_TIME'], 'time'),
        'wind_kt': (DL['WIND'], 'wind'),
        'wind_degrees': (DL['WIND_DIR'], 'wind_dir'),
        'davis_current_observation.wind_day_high_mph': (DL['WIND_MAX'], 'windmph'),
        # 'wind_dir_max': (DL['WIND_DIR_MAX'], 'wind_dir'),  # missing
        'davis_current_observation.wind_day_high_time': (DL['WIND_MAX_TIME'], 'time'),
        'davis_current_observation.rain_day_in': (DL['RAIN'], 'rainin'),
        'davis_current_observation.rain_rate_in_per_hr': (DL['RAIN_RATE'], 'rain_ratein'),
        'davis_current_observation.rain_rate_day_high_in_per_hr': (DL['RAIN_RATE_MAX'], 'rain_ratein'),
        # 'rain_rate_max_time': (DL['RAIN_RATE_MAX_TIME'], 'time'), # missing
        'davis_current_observation.rain_month_in': (DL['RAIN_MONTH'], 'rain_monthin'),
        'davis_current_observation.rain_year_in': (DL['RAIN_YEAR'], 'rain_yearin'),
    }

    def get_from_path(self, json, path):
        res = json
        parts = path.split('.')
        for part in parts:
            res = res[part]
        return res

    # temperature in Fahrenheit
    def _clean_tempf(self, value):
        return self._clean_temp((float(value) - 32) * 5 / 9)

    # dewpoint in Fahrenheit
    def _clean_dewf(self, value):
        return self._clean_dew((float(value) - 32) * 5 / 9)

    # pressure in inches of Hg
    def _clean_pressurein(self, value):
        return self._clean_pressure(float(value) * 33.8639)

    # wind in mph
    def _clean_windmph(self, value):
        return self._clean_wind(float(value) * 1.60934)

    # rain in inches
    def _clean_rainin(self, value):
        return self._clean_rain(float(value) * 25.4)

    # rain_rate in inches
    def _clean_rain_ratein(self, value):
        return self._clean_rain_rate(float(value) * 25.4)

    # rain_month in inches
    def _clean_rain_monthin(self, value):
        return self._clean_float(float(value) * 25.4)

    # rain_month in inches
    def _clean_rain_yearin(self, value):
        return self._clean_float(float(value) * 25.4)

    def parse(self, content, **kwargs):
        jsondata = json.loads(content)
        # datetime contained in a single field
        datetime = dateutil.parser.parse(jsondata['observation_time_rfc822'])
        data = {
            DL['DATE']: datetime.date(),
            DL['TIME']: datetime.time()
        }
        for k, i in self.data_map.items():
            try:
                value = str(self.get_from_path(jsondata, k))
                value = self._clean(value, i[1])
            except: # noqa
                value = None
            data[i[0]] = value
        return data
