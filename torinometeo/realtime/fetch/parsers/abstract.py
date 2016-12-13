import re
import datetime
from ..settings import EXTREMES as EX


class Parser(object):
    """ Parser class interface
        - parse: parses the given content and returns a python dict of data
    """

    non_decimal = re.compile(r'[^\d.]+')

    def __init__(self, **kwargs):
        self.time_format = kwargs.get('time_format') or '%H:%M'
        self.date_format = kwargs.get('date_format') or '%d/%m/%Y'

    def parse(self, content):
        raise NotImplementedError("Should have implemented this")

    def _to_float(self, value, precision=2):
        """ String to float rounded with precision
            Add here logic to support internalization
        """
        value = value.replace(',', '.')
        return round(float(self.non_decimal.sub('', value)), precision)

    def _to_float_extremes(self, value, var, precision=2):
        """ Checks float value agains extremes
        """
        aux = self._to_float(value)
        if aux > EX[var.upper()]['MAX'] or aux < EX[var.upper()]['MIN']:
            raise ValueError('wrong %s detected' % var)
        return aux

    def _clean(self, value, var):
        """ Clean data
            Entry point for cleaning data, just to avoid try catch repetition
            @TODO something more specific with exceptions?
        """
        try:
            value = getattr(self, '_clean_%s' % var)(value)
            return value
        except:
            # @TODO do something more specific with value errors?
            return None

    def _clean_float(self, value):
        return self._to_float(value)

    def _clean_temp(self, value):
        return self._to_float_extremes(value, 'temp')

    def _clean_time(self, value):
        return datetime.datetime.strptime(value.strip(), self.time_format).time() # noqa

    def _clean_date(self, value):
        return datetime.datetime.strptime(value.strip(), self.date_format).date() # noqa

    def _clean_humidity(self, value):
        return self._to_float_extremes(value, 'humidity')

    def _clean_dew(self, value):
        return self._to_float_extremes(value, 'dew')

    def _clean_pressure(self, value):
        return self._to_float_extremes(value, 'pressure')

    def _clean_wind(self, value):
        return self._to_float_extremes(value, 'wind')

    def _clean_wind_dir(self, value):
        try:
            aux = self._to_float(value)
        except:
            # some files may be html
            value = re.sub('[^nNsSoOwWeE]', '', value).rstrip()
            try:
                aux = EX['WIND_DIR']['TEXT'].index(value) * 22.5
            except:
                try:
                    aux = EX['WIND_DIR']['TEXT_I'].index(value) * 22.5
                except:
                    raise ValueError('wrong wind direction detected')
        return aux

    def _clean_rain(self, value):
        return self._to_float_extremes(value, 'rain')

    def _clean_rain_rate(self, value):
        return self._to_float_extremes(value, 'rain_rate')
