import json
import os
import re

from ..labels import DATA_LABELS as DL
from .abstract import Parser


class TmParser(Parser):

    # line num: (label, clean)
    data_map = {
        'measure_time': (DL['TIME'], 'time'),
        'measure_date': (DL['DATE'], 'date'),
        'temperature': (DL['TEMP'], 'temp'),
        'temperature_max': (DL['TEMP_MAX'], 'temp'),
        'temperature_max_time': (DL['TEMP_MAX_TIME'], 'time'),
        'temperature_min': (DL['TEMP_MIN'], 'temp'),
        'temperature_min_time': (DL['TEMP_MIN_TIME'], 'time'),
        'relative_humidity': (DL['HUMIDITY'], 'humidity'),
        'relative_humidity_max': (DL['HUMIDITY_MAX'], 'humidity'),
        'relative_humidity_max_time': (DL['HUMIDITY_MAX_TIME'], 'time'),
        'relative_himidity_min': (DL['HUMIDITY_MIN'], 'humidity'),
        'relative_humidity_min_time': (DL['HUMIDITY_MIN_TIME'], 'time'),
        'dewpoint': (DL['DEW'], 'dew'),
        'dewpoint_max': (DL['DEW_MAX'], 'dew'),
        'dewpoint_max_time': (DL['DEW_MAX_TIME'], 'time'),
        'dewpoint_min': (DL['DEW_MIN'], 'dew'),
        'dewpoint_min_time': (DL['DEW_MIN_TIME'], 'time'),
        'pressure': (DL['PRESSURE'], 'pressure'),
        'pressure_max': (DL['PRESSURE_MAX'], 'pressure'),
        'pressure_max_time': (DL['PRESSURE_MAX_TIME'], 'time'),
        'pressure_min': (DL['PRESSURE_MIN'], 'pressure'),
        'pressure_min_time': (DL['PRESSURE_MIN_TIME'], 'time'),
        'wind_strength': (DL['WIND'], 'wind'),
        'wind_dir': (DL['WIND_DIR'], 'wind_dir'),
        'wind_strength_max': (DL['WIND_MAX'], 'wind'),
        'wind_dir_max': (DL['WIND_DIR_MAX'], 'wind_dir'),
        'wind_max_time': (DL['WIND_MAX_TIME'], 'time'),
        'rain': (DL['RAIN'], 'rain'),
        'rain_rate': (DL['RAIN_RATE'], 'rain_rate'),
        'rain_rate_max': (DL['RAIN_RATE_MAX'], 'rain_rate'),
        'rain_rate_max_time': (DL['RAIN_RATE_MAX_TIME'], 'time'),
        'rain_month': (DL['RAIN_MONTH'], 'float'),
        'rain_year': (DL['RAIN_YEAR'], 'float'),
    }

    def parse(self, content):
        aux = re.sub(r"[\r\n\t\f\v]", r"", content)
        aux = re.sub(r",}", r"}", aux)
        jsondata = json.loads(aux)
        jsondata.update({'measure_time': jsondata['datetime']})
        jsondata.update({'measure_date': jsondata['datetime']})
        data = {}
        for k, i in self.data_map.iteritems():
            try:
                value = str(jsondata[k])
                value = self._clean(value, i[1])
            except: # noqa
                value = None
            data[i[0]] = value
        return data
