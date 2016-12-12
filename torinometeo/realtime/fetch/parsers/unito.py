import os

from .abstract import Parser
from ..labels import DATA_LABELS as DL


class UnitoParser(Parser):

    # line num: (label, clean)
    data_map = {
        1: (DL['DATE'], 'date'),
        2: (DL['TIME'], 'time'),
        4: (DL['TEMP'], 'temp'),
        5: (DL['TEMP_MAX'], 'temp'),
        6: (DL['TEMP_MAX_TIME'], 'time'),
        7: (DL['TEMP_MIN'], 'temp'),
        8: (DL['TEMP_MIN_TIME'], 'time'),
        10: (DL['HUMIDITY'], 'humidity'),
        11: (DL['HUMIDITY_MAX'], 'humidity'),
        12: (DL['HUMIDITY_MAX_TIME'], 'time'),
        13: (DL['HUMIDITY_MIN'], 'humidity'),
        14: (DL['HUMIDITY_MIN_TIME'], 'time'),
        16: (DL['DEW'], 'dew'),
        17: (DL['DEW_MAX'], 'dew'),
        18: (DL['DEW_MAX_TIME'], 'time'),
        19: (DL['DEW_MIN'], 'dew'),
        20: (DL['DEW_MIN_TIME'], 'time'),
        22: (DL['PRESSURE'], 'pressure'),
        23: (DL['PRESSURE_MAX'], 'pressure'),
        24: (DL['PRESSURE_MAX_TIME'], 'time'),
        25: (DL['PRESSURE_MIN'], 'pressure'),
        26: (DL['PRESSURE_MIN_TIME'], 'time'),
        28: (DL['WIND'], 'wind'),
        29: (DL['WIND_DIR'], 'wind_dir'),
        30: (DL['WIND_MAX'], 'wind'),
        31: (DL['WIND_DIR_MAX'], 'wind_dir'),
        32: (DL['WIND_MAX_TIME'], 'time'),
        # 34: (DL['RAIN_RATE'], 'rain_rate'),  # nd
        # 35: (DL['RAIN_RATE_MAX'], 'rain_rate'),  # nd
        # 36: (DL['RAIN_RATE_MAX_TIME'], 'time'),  # nd
        37: (DL['RAIN'], 'rain'),
        # 38: (DL['RAIN_MONTH'], 'float'),  # nd
        # 39: (DL['RAIN_YEAR'], 'float'),  # nd
    }

    def parse(self, content):
        lines = content.split(os.linesep)

        data = {}
        for k, i in self.data_map.iteritems():
            value = lines[k]
            value = self._clean(value, i[1])
            data[i[0]] = value

        return data

    def _clean_time(self, value):
        value = value[0:5]
        return super(UnitoParser, self)._clean_time(value)

    def _clean_humidity(self, value):
        value = value.split(' ')[0]
        return super(UnitoParser, self)._clean_humidity(value)

    def _clean_wind(self, value):
        value = float(value.split(' ')[0]) * 3.6
        return super(UnitoParser, self)._clean_wind(str(value))
