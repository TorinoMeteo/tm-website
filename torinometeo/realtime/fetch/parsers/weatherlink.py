import re
import datetime

from .abstract import Parser
from ..labels import DATA_LABELS as DL


class WeatherlinkParser(Parser):

    def parse(self, content):
        self.content = content

        data = {}
        data[DL['TIME']] = self._clean_time_timestamp(self.get_timestamp())
        data[DL['DATE']] = self._clean_date_timestamp(self.get_timestamp())

        temperatures = self.get_temperature()
        if temperatures:
            data[DL['TEMP']] = self._clean(temperatures[0], 'temp')
            data[DL['TEMP_MAX']] = self._clean(temperatures[1], 'temp')
            data[DL['TEMP_MAX_TIME']] = self._clean(temperatures[2], 'time')
            data[DL['TEMP_MIN']] = self._clean(temperatures[3], 'temp')
            data[DL['TEMP_MIN_TIME']] = self._clean(temperatures[4], 'time')

        humidity = self.get_humidity()
        if humidity:
            data[DL['HUMIDITY']] = self._clean(humidity[0], 'humidity')
            data[DL['HUMIDITY_MAX']] = self._clean(humidity[1], 'humidity')
            data[DL['HUMIDITY_MAX_TIME']] = self._clean(humidity[2], 'time')
            data[DL['HUMIDITY_MIN']] = self._clean(humidity[3], 'humidity')
            data[DL['HUMIDITY_MIN_TIME']] = self._clean(humidity[4], 'time')

        dew = self.get_dew()
        if dew:
            data[DL['DEW']] = self._clean(dew[0], 'dew')
            data[DL['DEW_MAX']] = self._clean(dew[1], 'dew')
            data[DL['DEW_MAX_TIME']] = self._clean(dew[2], 'time')
            data[DL['DEW_MIN']] = self._clean(dew[3], 'dew')
            data[DL['DEW_MIN_TIME']] = self._clean(dew[4], 'time')

        pressure = self.get_pressure()
        if pressure:
            data[DL['PRESSURE']] = self._clean(pressure[0], 'pressure')
            data[DL['PRESSURE_MAX']] = self._clean(pressure[1], 'pressure')
            data[DL['PRESSURE_MAX_TIME']] = self._clean(pressure[2], 'time')
            data[DL['PRESSURE_MIN']] = self._clean(pressure[3], 'pressure')
            data[DL['PRESSURE_MIN_TIME']] = self._clean(pressure[4], 'time')

        wind_strength = self.get_wind_strength()
        if wind_strength:
            data[DL['WIND']] = self._clean(wind_strength[0], 'wind')
            data[DL['WIND_MAX']] = self._clean(wind_strength[1], 'wind')
            data[DL['WIND_MAX_TIME']] = self._clean(wind_strength[2], 'time')

        wind_dir = self.get_wind_dir()
        if wind_dir:
            data[DL['WIND_DIR']] = self._clean(wind_dir[0], 'wind_dir')
            data[DL['WIND_DIR_MAX']] = None  # not provided

        rain = self.get_rain()
        if rain:
            data[DL['RAIN_RATE']] = self._clean(rain[0], 'rain')
            data[DL['RAIN']] = self._clean(rain[1], 'rain_rate')
            data[DL['RAIN_MONTH']] = self._clean(rain[2], 'float')
            data[DL['RAIN_YEAR']] = self._clean(rain[3], 'float')
            data[DL['RAIN_RATE_MAX']] = None  # not provided
            data[DL['RAIN_RATE_MAX_TIME']] = None  # not provided

        return data

    def get_timestamp(self):

        matches = re.search(
            'Current Conditions as of (\d+:\d+\s(?:[^ ]+),\s[^ ]+\s\d+,\s\d+)',  # noqa
            self.content,
            flags=re.IGNORECASE
        )
        if matches is not None:
            return matches.group(1)

    def _clean_time_timestamp(self, value):
        return datetime.datetime.strptime(value.strip(), '%H:%M %A, %B %d, %Y').time() # noqa

    def _clean_date_timestamp(self, value):
        return datetime.datetime.strptime(value.strip(), '%H:%M %A, %B %d, %Y').date() # noqa

    def get_temperature(self):

        matches = re.search(
            'Outside Temp.*\n.*?>([-\d.]+)\sC<.*\n.*?>([-\d.]+)\sC<.*\n.*?>([\d:]+)<.*\n.*?>([-\d.]+)\sC<.*\n.*?>([\d:]+)<', # noqa
            self.content,
            flags=re.MULTILINE
        )
        if matches is not None:
            return (
                matches.group(1),
                matches.group(2),
                matches.group(3),
                matches.group(4),
                matches.group(5),
            )
        return None

    def get_humidity(self):

        matches = re.search(
            'Outside Humidity.*\n.*?>([-\d.]+)%<.*\n.*?>([-\d.]+)%<.*\n.*?>([\d:]+)<.*\n.*?>([-\d.]+)%<.*\n.*?>([\d:]+)<', # noqa
            self.content,
            flags=re.MULTILINE
        )
        if matches is not None:
            return (
                matches.group(1),
                matches.group(2),
                matches.group(3),
                matches.group(4),
                matches.group(5),
            )
        return None

    def get_dew(self):

        matches = re.search(
            'Dew Point.*\n.*?>([-\d.]+)\sC<.*\n.*?>([-\d.]+)\sC<.*\n.*?>([\d:]+)<.*\n.*?>([-\d.]+)\sC<.*\n.*?>([\d:]+)<', # noqa
            self.content,
            flags=re.MULTILINE
        )
        if matches is not None:
            return (
                matches.group(1),
                matches.group(2),
                matches.group(3),
                matches.group(4),
                matches.group(5),
            )
        return None

    def get_pressure(self):

        matches = re.search(
            'Barometer.*\n.*?>([-\d.]+)[^<]+<.*\n.*?>([-\d.]+)[^<]+<.*\n.*?>([\d:]+)<.*\n.*?>([-\d.]+)[^<]+<.*\n.*?>([\d:]+)<', # noqa
            self.content,
            flags=re.MULTILINE
        )
        if matches is not None:
            return (
                matches.group(1),
                matches.group(2),
                matches.group(3),
                matches.group(4),
                matches.group(5),
            )
        return None

    def get_wind_strength(self):
        matches = re.search(
            'Wind Speed.*\n.*?>(.+?) ?(km/h)?<.*\n.*?>([-\d.]+) km/h<.*\n.*?>([\d:]+)<', # noqa
            self.content,
            flags=re.MULTILINE
        )
        if matches is not None:
            return (
                '0' if matches.group(1) == 'Calm' else matches.group(1),
                matches.group(3),
                matches.group(4),
            )
        return None

    def get_wind_dir(self):
        matches = re.search(
            'Wind Direction.*\n.*?>(.+?)<', # noqa
            self.content,
            flags=re.MULTILINE
        )
        if matches is not None:
            return (
                matches.group(1),
                None
            )
        return None

    def get_rain(self):

        matches = re.search(
            'Rain.*\n.*?>([-\d.]+)mm/Hour<.*\n.*?>([-\d.]+)mm<.*\n.*?>.*?<.*\n.*?>([-\d.]+)mm<.*\n.*?>([-\d.]+)mm<', # noqa
            self.content,
            flags=re.MULTILINE
        )
        if matches is not None:
            return (
                matches.group(1),
                matches.group(2),
                matches.group(3),
                matches.group(4),
            )
        return None
