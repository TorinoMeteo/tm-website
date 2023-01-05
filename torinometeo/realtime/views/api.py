import datetime
import json
import requests

from django.db.models import Max
from django.http import Http404
from django.utils import timezone
from django.conf import settings
from django.http import JsonResponse
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable

from realtime.models.stations import (Data, HistoricData, RadarSnapshot,
                                      Station, StationForecast, AirQualityStation)
from realtime.serializers import (HistoricDataSerializer, JustDataSerializer,
                                  RadarSnapshotSerializer,
                                  RealtimeDataSerializer,
                                  StationForecastSerializer, AirQualityStationSerializer)


class CurrentDayDataViewSet(viewsets.ViewSet):
    """ Realtime current day data
        Fetches the current day measured data of each station
    """

    def retrieve(self, request, pk=None):
        """
        Gets the current day measured data for the given station
        """
        try:
            today = timezone.datetime.today()
            station = Station.objects.get(active=True, slug=pk)
            data = Data.objects.filter(
                station__active=True,
                station=station,
                datetime__year=today.year,
                datetime__month=today.month,
                datetime__day=today.day).order_by('station__name').order_by(
                    'datetime')
            serializer = JustDataSerializer(
                data, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Station.DoesNotExist:
            raise Http404()


class LastRealtimeDataViewSet(viewsets.ViewSet):
    """ Realtime last data
        Fetches only the last measured data of each station
    """

    def list(self, request):
        """
        Gets the last fetched data
        """
        try:
            last_data = Data.objects.values('station').annotate(
                latest_id=Max('id'))
            ids = [d.get('latest_id') for d in last_data]
            data = Data.objects.filter(
                station__active=True, id__in=ids).order_by('station__name')
            serializer = RealtimeDataSerializer(
                data, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Data.DoesNotExist:
            raise Http404()

    def retrieve(self, request, pk=None):
        """
        Gets the last fetched data for the given station
        """
        try:
            station = Station.objects.get(active=True, slug=pk)
            data = Data.objects.filter(
                station=station).order_by('-datetime').first()
            serializer = RealtimeDataSerializer(
                data, many=False, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Station.DoesNotExist:
            raise Http404()


class HistoricDataViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ HistoricData
        Fetches historic data for a given date, if no date is given
        it fetches last
    """
    serializer_class = HistoricDataSerializer

    def get_queryset(self):
        try:
            date = datetime.datetime(
                year=int(self.kwargs['year']),
                month=int(self.kwargs['month']),
                day=int(self.kwargs['day']))
        except:
            date = datetime.date.fromordinal(
                datetime.date.today().toordinal() - 1)  # noqa

        return HistoricData.objects.filter(date=date).order_by('station__name')

class StationHistoricDataViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ StationHistoricData
        Fetches historic data for a given station and period
    """
    serializer_class = HistoricDataSerializer

    def get_queryset(self):
        try:
            from_date = datetime.datetime.fromtimestamp(int(self.request.query_params.get('from')))
            to_date = datetime.datetime.fromtimestamp(int(self.request.query_params.get('to')))
            station = get_object_or_404(Station, slug=self.kwargs.slug)
            return HistoricData.objects.filter(station=station, date__gte=from_date, date__lte=to_date).order_by('station__name')
        except:
            raise NotAcceptable('Wrong params')

class RadarSnapshotViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ Radar snapshot
    """
    serializer_class = RadarSnapshotSerializer

    def get_queryset(self):
        try:
            date = datetime.datetime(
                year=int(self.kwargs['year']),
                month=int(self.kwargs['month']),
                day=int(self.kwargs['day']))
        except:
            date = datetime.date.today()

        return RadarSnapshot.objects.filter(
            datetime__startswith=date.date()).order_by('datetime')  # noqa


class StationForecastViewSet(viewsets.ModelViewSet):
    """ StationForecast CRUD
        Allows to create, edit and delete station forecasts
        GET is public, POST, PUT, PATCH and DELETE require authentication
    """
    queryset = StationForecast.objects.all()
    serializer_class = StationForecastSerializer

    def get_permissions(self):
        """
        GET requests allowed to every one
        POST requests require the user to have the add permission on the model. # noqa
        PUT and PATCH requests require the user to have the change permission on the model. # noqa
        DELETE requests require the user to have the delete permission on the model. # noqa
        """
        return (permissions.DjangoModelPermissionsOrAnonReadOnly(), )

    def get_queryset(self):
        """ Looks for date param in order to filter only related forecasts
            The date param is mandatory! otherwise it will return an empty queryset
            to avoid timeout issues (too many records)
        """
        queryset = StationForecast.objects.all()
        station_slug = self.request.query_params.get('station', None)
        if station_slug is not None:
            queryset = queryset.filter(station__slug=station_slug)
        date = self.request.query_params.get('date', None)
        if date is not None:
            queryset = queryset.filter(date=date)
        else:
            return StationForecast.objects.none()
        return queryset

    @list_route()
    def next(self, request):
        queryset = StationForecast.objects.filter(
            date__gte=datetime.datetime.now()).order_by('date')
        station_slug = self.request.query_params.get('station', None)
        if station_slug is not None:
            queryset = queryset.filter(station__slug=station_slug).distinct()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AirQualityStationViewSet(viewsets.ModelViewSet):
    """ Air Quality Station viewset
        Fetches all the active air quality stations
    """
    queryset = AirQualityStation.objects.active()
    serializer_class = AirQualityStationSerializer

    def get_permissions(self):
        """
        GET requests allowed to every one
        POST requests require the user to have the add permission on the model. # noqa
        PUT and PATCH requests require the user to have the change permission on the model. # noqa
        DELETE requests require the user to have the delete permission on the model. # noqa
        """
        return (permissions.DjangoModelPermissionsOrAnonReadOnly(), )


class VCOApi(APIView):
    def get(self, request):
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        init = (datetime.datetime.now() - datetime.timedelta(hours=2)).replace(minute=0, second=0)
        end = (init + datetime.timedelta(days=9)).replace(hour=23, minute=59, second=59, microsecond=999999)
        r = requests.get('https://api.meteomatics.com/%s--%s:PT1H/t_2m:C,precip_1h:mm,wind_speed_10m:kmh,wind_dir_10m:d,weather_symbol_1h:idx/%s,%s/json?model=mix' % (
            init.replace(tzinfo=datetime.timezone.utc).isoformat(),
            end.replace(tzinfo=datetime.timezone.utc).isoformat(),
            lat,
            lng
        ), auth=(settings.VCO_USER, settings.VCO_PWD))

        return JsonResponse(json.loads(r.text))
