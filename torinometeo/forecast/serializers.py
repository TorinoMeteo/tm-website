from rest_framework import serializers

from forecast.models import Forecast, DayForecast

class DayForecastSerializer(serializers.ModelSerializer):
    """ Day Forecast Serializer
    """
    class Meta:
        model = DayForecast
        fields = ('forecast', 'date', 'image12', 'image24', 'text', 'temperatures', 'winds', 'reliability')

class ForecastSerializer(serializers.ModelSerializer):
    """ Forecast Serializer
    """
    day_forecasts = DayForecastSerializer(source='dayforecast_set', read_only=True, many=True)
    class Meta:
        model = Forecast
        fields = ('id', 'date', 'pattern', 'day_forecasts')
        read_only_fields = ('day_forecasts',)

