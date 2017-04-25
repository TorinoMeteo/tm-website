from rest_framework import serializers

from .models.stations import Data, Station


class StationSerializer(serializers.ModelSerializer):
    """ Realtime Station Serializer
    """
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Station
        fields = (
            'id',
            'name',
            'nation',
            'region',
            'province',
            'city',
            'image_url',
            'webcam',
        )
        depth = 1

    def get_image_url(self, station):
        request = self.context.get('request')
        image_url = station.image.url
        return request.build_absolute_uri(image_url)


class RealtimeDataSerializer(serializers.ModelSerializer):
    """ Realtime Data Serializer
    """
    station = StationSerializer()

    class Meta:
        model = Data
        fields = (
            'station',
            'datetime',
            'temperature',
            'temperature_max',
            'temperature_max_time',
            'temperature_min',
            'temperature_min_time',
            'relative_humidity',
            'relative_humidity_max',
            'relative_humidity_max_time',
            'relative_humidity_min',
            'relative_humidity_min_time',
            'dewpoint',
            'dewpoint_max',
            'dewpoint_max_time',
            'dewpoint_min',
            'dewpoint_min_time',
            'pressure',
            'pressure_max',
            'pressure_max_time',
            'pressure_min',
            'pressure_min_time',
            'wind_strength',
            'wind_dir',
            'wind_strength_max',
            'wind_dir_max',
            'wind_max_time',
            'rain',
            'rain_rate',
            'rain_rate_max',
            'rain_rate_max_time',
            'rain_month',
            'rain_year'
        )
