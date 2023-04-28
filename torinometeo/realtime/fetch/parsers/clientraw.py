from .abstract import Parser
from ..labels import DATA_LABELS as DL


class ClientrawParser(Parser):

    # line num: (label, clean)
    data_map = {
        74: (DL['DATE'], 'date'),
        4: (DL['TEMP'], 'temp'),
        46: (DL['TEMP_MAX'], 'temp'),
        47: (DL['TEMP_MIN'], 'temp'),
        5: (DL['HUMIDITY'], 'humidity'),
        72: (DL['DEW'], 'dew'),
        138: (DL['DEW_MAX'], 'dew'),
        139: (DL['DEW_MIN'], 'dew'),
        6: (DL['PRESSURE'], 'pressure'),
        131: (DL['PRESSURE_MAX'], 'pressure'),
        132: (DL['PRESSURE_MIN'], 'pressure'),
        1: (DL['WIND'], 'wind'),
        3: (DL['WIND_DIR'], 'wind_dir'),
        71: (DL['WIND_MAX'], 'wind'),
        117: (DL['WIND_DIR_MAX'], 'wind_dir'),
        7: (DL['RAIN'], 'rain'),
        10: (DL['RAIN_RATE'], 'rain_rate'),
        11: (DL['RAIN_RATE_MAX'], 'rain_rate'),
        8: (DL['RAIN_MONTH'], 'float'),
        9: (DL['RAIN_YEAR'], 'float')
    }

    def parse(self, content, **kwargs):

        rawdata = content.split(' ')
        rawdata.append(str(rawdata[29]) + ':' + str(rawdata[30]))
        self.data_map.update({int(len(rawdata)-1): (DL['TIME'], 'time')})

        data = {}
        for k, i in self.data_map.items():
            value = rawdata[k]
            value = self._clean(value, i[1])
            data[i[0]] = value
        return data
