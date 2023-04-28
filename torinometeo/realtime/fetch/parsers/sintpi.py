import json

from .abstract import Parser
from ..labels import DATA_LABELS as DL


class SintpiParser(Parser):

    # line num: (label, clean)
    data_map = {
        'measure_time': (DL['TIME'], 'time'),
        'measure_date': (DL['DATE'], 'date'),
        'temp_out': (DL['TEMP'], 'temp'),
        'TempOutMax': (DL['TEMP_MAX'], 'temp'),
        'TempOutMin': (DL['TEMP_MIN'], 'temp'),
        'hum_out': (DL['HUMIDITY'], 'humidity'),
        'UmOutMax': (DL['HUMIDITY_MAX'], 'humidity'),
        'UmOutMin': (DL['HUMIDITY_MIN'], 'humidity'),
        'dew_point': (DL['DEW'], 'dew'),
        'rel_pressure': (DL['PRESSURE'], 'pressure'),
        'PressureMax': (DL['PRESSURE_MAX'], 'pressure'),
        'PressureMin': (DL['PRESSURE_MIN'], 'pressure'),
        'wind_gust': (DL['WIND'], 'wind'),
        'wind_dir': (DL['WIND_DIR'], 'wind_dir'),
        'winDayGustMax': (DL['WIND_MAX'], 'wind'),
        'wind_dir_ave': (DL['WIND_DIR_MAX'], 'wind_dir'),
        'rain_rate': (DL['RAIN'], 'rain'),
        'rain_rate_1h': (DL['RAIN_RATE'], 'rain_rate'),
        'rain': (DL['RAIN_YEAR'], 'float'),
    }

    def parse(self, content, **kwargs):

        jsondata = json.loads(content)
        jsondata.update({'measure_time': jsondata['last_measure_time']})
        jsondata.update({'measure_date': jsondata['last_measure_time']})
#        jsondata.update({'today_rain': float(jsondata['rain_rate_24h'])*24.0})


        data = {}
        for k, i in self.data_map.items():
            value = str(jsondata[k])
            value = self._clean(value, i[1])
            data[i[0]] = value
        return data
