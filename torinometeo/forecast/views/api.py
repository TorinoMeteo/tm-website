from django.http import Http404

from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import list_route

from forecast.models import Forecast, DayForecast
from forecast.serializers import ForecastSerializer, DayForecastSerializer


class ForecastViewSet(viewsets.ModelViewSet):
    """ Forecast CRUD
        Allows to create, edit and delete forecasts

        get-last fetches only the last forecast

        GET is public, POST, PUT, PATCH and DELETE require authentication
    """
    lookup_field = 'id'
    queryset = Forecast.objects.all()
    serializer_class = ForecastSerializer

    def get_permissions(self):
        """
        GET requests allowed to every one
        POST requests require the user to have the add permission on
        the model.
        PUT and PATCH requests require the user to have the change permission on the model. # noqa
        DELETE requests require the user to have the delete permission on the model. # noqa
        """
        return (permissions.DjangoModelPermissionsOrAnonReadOnly(), )

    @list_route(methods=['get'], url_path="get-last")
    def get_last(self, request, id=None, pk=None):
        """
        Gets the last forecast
        """
        try:
            forecast = Forecast.objects.latest('date')
            serializer = ForecastSerializer(forecast)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Forecast.DoesNotExist:
            raise Http404()


class DayForecastViewSet(viewsets.ModelViewSet):
    """ Day Forecast CRUD
        Allows to create, edit and delete day forecasts
        GET is public, POST, PUT, PATCH and DELETE require authentication
    """
    lookup_field = 'date'
    queryset = DayForecast.objects.all()
    serializer_class = DayForecastSerializer

    def get_permissions(self):
        """
        GET requests allowed to every one
        POST requests require the user to have the add permission on the model. # noqa
        PUT and PATCH requests require the user to have the change permission on the model. # noqa
        DELETE requests require the user to have the delete permission on the model. # noqa
        """
        return (permissions.DjangoModelPermissionsOrAnonReadOnly(), )

    def get_queryset(self):
        """ Looks for forecast param in order to filter only related day forecasts
        """
        queryset = DayForecast.objects.all()
        forecast_id = self.request.query_params.get('forecast', None)
        if forecast_id is not None:
            queryset = queryset.filter(forecast__id=forecast_id)
        return queryset
