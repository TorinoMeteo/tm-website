import json
import os
import re

from ..labels import AIRQUALITY_DATA_LABELS as DL
from .abstract import Parser


class AirqualityParser(Parser):

    # line num: (label, clean)
    data_map = {
        'datetime': (DL['DATETIME'], 'datetime'),
        'air_quality_index': (DL['AIR_QUALITY_INDEX'], 'int'),
        'pm1': (DL['PM1'], 'pm'),
        'pm1_max': (DL['PM1_MAX'], 'pm'),
        'pm1_max_time': (DL['PM1_MAX_TIME'], 'time'),
        'pm1_min': (DL['PM1_MIN'], 'pm'),
        'pm1_min_time': (DL['PM1_MIN_TIME'], 'time'),
        'pm2_5': (DL['PM25'], 'pm'),
        'pm2_5_max': (DL['PM25_MAX'], 'pm'),
        'pm2_5_max_time': (DL['PM25_MAX_TIME'], 'time'),
        'pm2_5_min': (DL['PM25_MIN'], 'pm'),
        'pm2_5_min_time': (DL['PM25_MIN_TIME'], 'time'),
        'pm10': (DL['PM10'], 'pm'),
        'pm10_max': (DL['PM10_MAX'], 'pm'),
        'pm10_max_time': (DL['PM10_MAX_TIME'], 'time'),
        'pm10_min': (DL['PM10_MIN'], 'pm'),
        'pm10_min_time': (DL['PM10_MIN_TIME'], 'time'),
    }

    def parse(self, content):
        aux = re.sub(r"[\r\n\t\f\v]", r"", content)
        aux = re.sub(r",}", r"}", aux)
        jsondata = json.loads(aux)
        data = {}
        for k, i in self.data_map.items():
            try:
                value = str(jsondata[k])
                value = self._clean(value, i[1])
            except: # noqa
                value = None
            data[i[0]] = value

        return data
