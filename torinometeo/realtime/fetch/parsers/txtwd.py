import os
import re

from .abstract import Parser
from ..labels import DATA_LABELS as DL


class TxtwdParser(Parser):

    # line num: (label, clean)
    data_map = {
        1: (DL['TIME'], 'time'),
        2: (DL['DATE'], 'date'),
        4: (DL['TEMP'], 'temp'),
        5: (DL['TEMP_MAX'], 'temp'),
        6: (DL['TEMP_MAX_TIME'], 'time'),
        7: (DL['TEMP_MIN'], 'temp'),
        8: (DL['TEMP_MIN_TIME'], 'time'),
        16: (DL['HUMIDITY'], 'humidity'),
        17: (DL['HUMIDITY_MAX'], 'humidity'),
        18: (DL['HUMIDITY_MAX_TIME'], 'time'),
        19: (DL['HUMIDITY_MIN'], 'humidity'),
        20: (DL['HUMIDITY_MIN_TIME'], 'time'),
        22: (DL['DEW'], 'dew'),
        23: (DL['DEW_MAX'], 'dew'),
        24: (DL['DEW_MAX_TIME'], 'time'),
        25: (DL['DEW_MIN'], 'dew'),
        26: (DL['DEW_MIN_TIME'], 'time'),
        28: (DL['PRESSURE'], 'pressure'),
        29: (DL['PRESSURE_MAX'], 'pressure'),
        30: (DL['PRESSURE_MAX_TIME'], 'time'),
        31: (DL['PRESSURE_MIN'], 'pressure'),
        32: (DL['PRESSURE_MIN_TIME'], 'time'),
        34: (DL['WIND'], 'wind'),
        35: (DL['WIND_DIR'], 'wind_dir'),
        36: (DL['WIND_MAX'], 'wind'),
        37: (DL['WIND_DIR_MAX'], 'wind_dir'),
        38: (DL['WIND_MAX_TIME'], 'time'),
        40: (DL['RAIN'], 'rain'),
        41: (DL['RAIN_RATE'], 'rain_rate'),
        42: (DL['RAIN_RATE_MAX'], 'rain_rate'),
        43: (DL['RAIN_RATE_MAX_TIME'], 'time'),
        44: (DL['RAIN_MONTH'], 'float'),
        45: (DL['RAIN_YEAR'], 'float'),
    }

    def parse(self, content):
        lines = content.split(os.linesep)
        
        data = {}
        for k, i in self.data_map.items():
            # remove html tags
            value = re.sub('<[^<]+?>', '', lines[k]).rstrip()
            value = self._clean(value, i[1])
            data[i[0]] = value

        print("DATA")
        print(data)

        return data
