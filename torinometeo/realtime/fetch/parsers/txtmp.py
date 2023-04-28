import os
import re

from .abstract import Parser
from ..labels import DATA_LABELS as DL


class TxtmpParser(Parser):

    # line num: (label, clean)
    data_map = {
        0: (DL['DATE'], 'date'),
        1: (DL['TIME'], 'time'),
        2: (DL['TEMP'], 'temp'),
        3: (DL['TEMP_MAX'], 'temp'),
        4: (DL['TEMP_MAX_TIME'], 'time'),
        5: (DL['TEMP_MIN'], 'temp'),
        6: (DL['TEMP_MIN_TIME'], 'time'),
        7: (DL['HUMIDITY'], 'humidity'),
        8: (DL['HUMIDITY_MAX'], 'humidity'),
        9: (DL['HUMIDITY_MAX_TIME'], 'time'),
        10: (DL['HUMIDITY_MIN'], 'humidity'),
        11: (DL['HUMIDITY_MIN_TIME'], 'time'),
        12: (DL['DEW'], 'dew'),
        13: (DL['DEW_MAX'], 'dew'),
        14: (DL['DEW_MAX_TIME'], 'time'),
        15: (DL['DEW_MIN'], 'dew'),
        16: (DL['DEW_MIN_TIME'], 'time'),
        29: (DL['PRESSURE'], 'pressure'),
        31: (DL['PRESSURE_MAX'], 'pressure'),
        32: (DL['PRESSURE_MAX_TIME'], 'time'),
        33: (DL['PRESSURE_MIN'], 'pressure'),
        34: (DL['PRESSURE_MIN_TIME'], 'time'),
        23: (DL['WIND'], 'wind'),
        27: (DL['WIND_DIR'], 'wind_dir'),
        24: (DL['WIND_MAX'], 'wind'),
        25: (DL['WIND_MAX_TIME'], 'time'),
        35: (DL['RAIN'], 'rain'),
        36: (DL['RAIN_RATE'], 'rain_rate'),
        37: (DL['RAIN_MONTH'], 'float'),
        38: (DL['RAIN_YEAR'], 'float'),
    }

    def parse(self, content, **kwargs):
        lines = content.split(os.linesep)
        
        data = {}
        for k, i in self.data_map.items():
            # remove html tags
            value = re.sub('<[^<]+?>', '', lines[k]).rstrip()
            value = self._clean(value, i[1])
            data[i[0]] = value

        return data
