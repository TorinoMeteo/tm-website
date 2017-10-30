from rest_framework import serializers

from .models.stations import Data, Station, HistoricData, RadarSnapshot, \
    Weather, ForecastWeather


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
    weather_icon_url = serializers.SerializerMethodField()

    class Meta:
        model = Data
        fields = (
            'station',
            'weather_icon_url',
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
            'wind_dir_text',
            'wind_strength_max',
            'wind_dir_max',
            'wind_dir_max_text',
            'wind_max_time',
            'rain',
            'rain_rate',
            'rain_rate_max',
            'rain_rate_max_time',
            'rain_month',
            'rain_year'
        )

    def get_weather_icon_url(self, data):
        try:
            weather = Weather.objects.filter(
                station=data.station
            ).order_by('-last_updated').first()
            return weather.icon
        except:
            return None


class HistoricDataSerializer(serializers.ModelSerializer):
    """ Realtime Data Serializer
    """
    station = StationSerializer()

    class Meta:
        model = HistoricData
        fields = (
            'station',
            'date',
            'temperature_mean',
            'temperature_max',
            'temperature_min',
            'relative_humidity_mean',
            'relative_humidity_max',
            'relative_humidity_min',
            'pressure_mean',
            'pressure_max',
            'pressure_min',
            'rain'
        )


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
        return 'http://radar.torinometeo.org/images/%s' % snapshot.filename


class ForecastWeatherSerializer(serializers.ModelSerializer):
    """ Forecast Weather Serializer
    """
    class Meta:
        model = ForecastWeather
        fields = (
            'station',
            'date',
            'icon',
            'text',
        )
