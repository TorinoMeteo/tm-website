import re
import datetime
from ..settings import EXTREMES as EX


class Parser(object):
    """ Parser class interface
        - parse: parses the given content and returns a python dict of data
    """

    non_decimal = re.compile(r'[^\d.]+')

    def __init__(self, **kwargs):
        self.time_format = kwargs.get('time_format') or '%H:%M %p'
        self.date_format = kwargs.get('date_format') or '%d/%m/%Y'

    def parse(self, content):
        raise NotImplementedError("Should have implemented this")

    def _clean_float(self, value):
        try:
            aux = round(float(self.non_decimal.sub('', value)), 2)
        except:
            aux = None
        return aux

    def _clean_temp(self, value):
        try:
            aux = round(float(self.non_decimal.sub('', value)), 2)
            if (aux > EX['TEMP']['MAX']) or (aux < EX['TEMP']['MIN']):
                aux = None
        except:
            aux = None
        return aux

    def _clean_time(self, value):
        try:
            aux = datetime.datetime.strptime(value.strip(), self.time_format).time() # noqa
        except:
            aux = None
        return aux

    def _clean_date(self, value):
        try:
            aux = datetime.datetime.strptime(value.strip(), self.date_format).date() # noqa
        except:
            aux = None
        return aux

    def _clean_humidity(self, value):
        try:
            aux = round(float(self.non_decimal.sub('', value)), 2)
            if (aux > EX['HUMIDITY']['MAX']) or (aux < EX['HUMIDITY']['MIN']):
                aux = None
        except:
            aux = None
        return aux

    def _clean_dew(self, value):
        try:
            aux = round(float(self.non_decimal.sub('', value)), 2)
            if (aux > EX['DEW']['MAX']) or (aux < EX['DEW']['MIN']):
                aux = None
        except:
            aux = None
        return aux

    def _clean_pressure(self, value):
        try:
            aux = round(float(self.non_decimal.sub('', value)), 2)
            if (aux > EX['PRESSURE']['MAX']) or (aux < EX['PRESSURE']['MIN']):
                aux = None
        except:
            aux = None
        return aux

    def _clean_wind(self, value):
        try:
            aux = round(float(self.non_decimal.sub('', value)), 2)
            if (aux > EX['WIND']['MAX']) or (aux < EX['WIND']['MIN']):
                aux = None
        except:
            aux = None
        return aux

    def _clean_wind_dir(self, value):
        try:
            aux = round(float(self.non_decimal.sub('', value)), 2)
        except:
            try:
                aux = EX['WIND_DIR']['TEXT'].index(str(value).rstrip()) * 22.5
            except:
                pass
            try:
                aux = EX['WIND_DIR']['TEXT_I'].index(str(value).rstrip()) * 22.5 # noqa
            except:
                aux = None
        return aux

    def _clean_rain(self, value):
        try:
            aux = round(float(self.non_decimal.sub('', value)), 2)
            if (aux > EX['RAIN']['MAX']) or (aux < EX['RAIN']['MIN']):
                aux = None
        except:
            aux = None
        return aux

    def _clean_rain_rate(self, value):
        try:
            aux = round(float(self.non_decimal.sub('', value)), 2)
            if (aux > EX['RAIN_RATE']['MAX']) or (aux < EX['RAIN_RATE']['MIN']): # noqa
                aux = None
        except:
            aux = None
        return aux
