import os

from .abstract import Parser
from ..labels import DATA_LABELS as DL


class UnitoParser(Parser):

    # line num: (label, clean)
    data_map = {
        4: (DL['DATE'], 'date'),
        5: (DL['TIME'], 'time'),
        7: (DL['TEMP'], 'temp'),
        8: (DL['TEMP_MAX'], 'temp'),
        9: (DL['TEMP_MAX_TIME'], 'time'),
        10: (DL['TEMP_MIN'], 'temp'),
        11: (DL['TEMP_MIN_TIME'], 'time'),
        13: (DL['HUMIDITY'], 'humidity'),
        14: (DL['HUMIDITY_MAX'], 'humidity'),
        15: (DL['HUMIDITY_MAX_TIME'], 'time'),
        16: (DL['HUMIDITY_MIN'], 'humidity'),
        17: (DL['HUMIDITY_MIN_TIME'], 'time'),
        19: (DL['DEW'], 'dew'),
        20: (DL['DEW_MAX'], 'dew'),
        21: (DL['DEW_MAX_TIME'], 'time'),
        22: (DL['DEW_MIN'], 'dew'),
        23: (DL['DEW_MIN_TIME'], 'time'),
        25: (DL['PRESSURE'], 'pressure'),
        26: (DL['PRESSURE_MAX'], 'pressure'),
        27: (DL['PRESSURE_MAX_TIME'], 'time'),
        28: (DL['PRESSURE_MIN'], 'pressure'),
        29: (DL['PRESSURE_MIN_TIME'], 'time'),
        31: (DL['WIND'], 'wind'),
        32: (DL['WIND_DIR'], 'wind_dir'),
        33: (DL['WIND_MAX'], 'wind'),
        34: (DL['WIND_DIR_MAX'], 'wind_dir'),
        35: (DL['WIND_MAX_TIME'], 'time'),
        # 34: (DL['RAIN_RATE'], 'rain_rate'),  # nd
        # 35: (DL['RAIN_RATE_MAX'], 'rain_rate'),  # nd
        # 36: (DL['RAIN_RATE_MAX_TIME'], 'time'),  # nd
        40: (DL['RAIN'], 'rain'),
        # 38: (DL['RAIN_MONTH'], 'float'),  # nd
        # 39: (DL['RAIN_YEAR'], 'float'),  # nd
    }

    def parse(self, content, **kwargs):
        f_lines = content.split(os.linesep)
        lines = []
        for line in f_lines:
            if line != '' and line != '\r':
                lines.append(line)

        data = {}
        for k, i in self.data_map.items():
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
