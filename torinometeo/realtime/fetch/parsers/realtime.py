from .abstract import Parser
from ..labels import DATA_LABELS as DL

#cumulus Realtime.txt parser
class RealtimeParser(Parser):

    # line num: (label, clean)
    data_map = {
        0: (DL['DATE'], 'date'),
        1: (DL['TIME'], 'time'),
        2: (DL['TEMP'], 'temp'),
        26: (DL['TEMP_MAX'], 'temp'),
        27: (DL['TEMP_MAX_TIME'], 'time'),
        28: (DL['TEMP_MIN'], 'temp'),
        29: (DL['TEMP_MIN_TIME'], 'time'),
        3: (DL['HUMIDITY'], 'humidity'),
        4: (DL['DEW'], 'dew'),
        10: (DL['PRESSURE'], 'pressure'),
        34: (DL['PRESSURE_MAX'], 'pressure'),
        35: (DL['PRESSURE_MAX_TIME'], 'time'),
        36: (DL['PRESSURE_MIN'], 'pressure'),
        37: (DL['PRESSURE_MAX_TIME'], 'time'),
        40: (DL['WIND'], 'wind'),
        11: (DL['WIND_DIR'], 'wind_dir'),
        32: (DL['WIND_MAX'], 'wind'),
        51: (DL['WIND_DIR_MAX'], 'wind_dir'),
        33: (DL['WIND_MAX_TIME'], 'time'),
        9: (DL['RAIN'], 'rain'),
        8: (DL['RAIN_RATE'], 'rain_rate'),
        19: (DL['RAIN_MONTH'], 'float'),
        20: (DL['RAIN_YEAR'], 'float'),
    }

    def parse(self, content, **kwargs):
        rawdata = content.split(' ')
        data = {}
        for k, i in self.data_map.items():
            value = rawdata[k]
            value = self._clean(value, i[1])
            data[i[0]] = value
        return data
