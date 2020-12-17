from django.conf import settings
from rest_framework import serializers

from .models.stations import (Data, HistoricData, RadarSnapshot, Station,
                              StationForecast, AirQualityStation)


class StationSerializer(serializers.ModelSerializer):
    """ Realtime Station Serializer
    """
    image_url = serializers.SerializerMethodField()
    webcam_url = serializers.SerializerMethodField()

    class Meta:
        model = Station
        fields = (
            'id',
            'slug',
            'name',
            'description',
            'climate',
            'nation',
            'region',
            'province',
            'city',
            'lat',
            'lng',
            'elevation',
            'image_url',
            'webcam',
            'webcam_url',
        )
        depth = 1

    def get_image_url(self, station):
        if not station.image:
            return None
        request = self.context.get('request')
        image_url = station.image.url
        return request.build_absolute_uri(image_url)

    def get_webcam_url(self, station):
        if not station.webcam:
            return None
        request = self.context.get('request')
        image_url = '/realtime/webcam/%d' % station.id
        return request.build_absolute_uri(image_url)


class RealtimeDataSerializer(serializers.ModelSerializer):
    """ Realtime Data Serializer
    """
    station = StationSerializer()
    weather_icon = serializers.SerializerMethodField()
    weather_icon_credits = serializers.SerializerMethodField()

    class Meta:
        model = Data
        fields = ('station', 'weather_icon', 'weather_icon_credits',
                  'datetime', 'temperature', 'temperature_max',
                  'temperature_max_time', 'temperature_min',
                  'temperature_min_time', 'relative_humidity',
                  'relative_humidity_max', 'relative_humidity_max_time',
                  'relative_humidity_min', 'relative_humidity_min_time',
                  'dewpoint', 'dewpoint_max', 'dewpoint_max_time',
                  'dewpoint_min', 'dewpoint_min_time', 'pressure',
                  'pressure_max', 'pressure_max_time', 'pressure_min',
                  'pressure_min_time', 'wind_strength', 'wind_dir',
                  'wind_dir_text', 'wind_strength_max', 'wind_dir_max',
                  'wind_dir_max_text', 'wind_max_time', 'rain', 'rain_rate',
                  'rain_rate_max', 'rain_rate_max_time', 'rain_month',
                  'rain_year')

    def get_weather_icon(self, data):
        return data.station.weather_icon()

    def get_weather_icon_credits(self, f):
        if f.station.forecast_url:
            return f.station.forecast_url.replace('forecast.xml', '')
        return None


class JustDataSerializer(serializers.ModelSerializer):
    """ Realtime Just Data Serializer
    """
    class Meta:
        model = Data
        fields = ('datetime', 'temperature', 'temperature_max',
                  'temperature_max_time', 'temperature_min',
                  'temperature_min_time', 'relative_humidity',
                  'relative_humidity_max', 'relative_humidity_max_time',
                  'relative_humidity_min', 'relative_humidity_min_time',
                  'dewpoint', 'dewpoint_max', 'dewpoint_max_time',
                  'dewpoint_min', 'dewpoint_min_time', 'pressure',
                  'pressure_max', 'pressure_max_time', 'pressure_min',
                  'pressure_min_time', 'wind_strength', 'wind_dir',
                  'wind_dir_text', 'wind_strength_max', 'wind_dir_max',
                  'wind_dir_max_text', 'wind_max_time', 'rain', 'rain_rate',
                  'rain_rate_max', 'rain_rate_max_time', 'rain_month',
                  'rain_year')


class HistoricDataSerializer(serializers.ModelSerializer):
    """ Realtime Data Serializer
    """
    station = StationSerializer()

    class Meta:
        model = HistoricData
        fields = ('station', 'date', 'temperature_mean', 'temperature_max',
                  'temperature_min', 'relative_humidity_mean',
                  'relative_humidity_max', 'relative_humidity_min',
                  'pressure_mean', 'pressure_max', 'pressure_min', 'rain')


class RadarSnapshotSerializer(serializers.ModelSerializer):
    """ Radar images Serializer
    """
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = RadarSnapshot
        fields = (
            'filename',
            'datetime',
            'file_url',
        )

    def get_file_url(self, snapshot):
        return 'https://radar.torinometeo.org/images/%s' % snapshot.filename


class StationForecastSerializer(serializers.ModelSerializer):
    """ Station Forecast Serializer
    """
    period = serializers.SerializerMethodField()
    icon = serializers.SerializerMethodField()
    credits = serializers.SerializerMethodField()

    class Meta:
        model = StationForecast
        fields = (
            'last_edit',
            'date',
            'period',
            'icon',
            'text',
            'credits',
        )

    def get_period(self, f):
        return f.get_period_display()

    def get_icon(self, f):
        return '%s%s.png' % (settings.BASE_WEATHER_ICON_URL, f.icon)

    def get_credits(self, f):
        if f.station.forecast_url:
            return f.station.forecast_url.replace('forecast.xml', '')
        return None


class AirQualityStationSerializer(serializers.ModelSerializer):
    """ Air Quality Station Serializer
    """
    class Meta:
        model = AirQualityStation
        fields = (
            'id',
            'slug',
            'name',
            'description',
            'nation',
            'region',
            'province',
            'city',
            'lat',
            'lng',
            'elevation',
            'data_url',
        )
        depth = 1
