import json

from .abstract import Parser
from ..labels import DATA_LABELS as DL
from bs4 import BeautifulSoup
import aprslib
import datetime

class AprsParser(Parser):

    # line num: (label, clean)
    data_map = {
        'measure_time': (DL['TIME'], 'time'),
        'measure_date': (DL['DATE'], 'date'),
        'temperature': (DL['TEMP'], 'temp'),
        'dew_point': (DL['DEW'], 'dew'),
        'humidity': (DL['HUMIDITY'], 'humidity'),
        'pressure': (DL['PRESSURE'], 'pressure'),
        'wind_gust': (DL['WIND'], 'wind'),
        'wind_direction': (DL['WIND_DIR'], 'wind_dir'),
        'rain_since_midnight': (DL['RAIN'], 'rain'),
    }

    def parse(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        results = soup.get_text().rstrip().splitlines()[-1]
        aprsData = aprslib.parse(results)
        weatherData = aprsData['weather']
        weatherData.update({'measure_time': datetime.datetime.fromtimestamp(int(aprsData['timestamp'])).strftime('%H:%M')})
        weatherData.update({'measure_date': datetime.datetime.fromtimestamp(int(aprsData['timestamp'])).strftime('%d/%m/%Y')})
        dew = (float(weatherData['humidity'])/100)**(1.0/8.0)*(112.0+0.9*float(weatherData['temperature']))+0.1*float(weatherData['temperature'])-112
        weatherData.update({'dew_point': dew})

        data = {}
        for k, i in self.data_map.iteritems():
            value = str(weatherData[k])
            value = self._clean(value, i[1])
            data[i[0]] = value
        return data
