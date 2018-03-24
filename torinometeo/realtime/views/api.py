import datetime

from django.db.models import Max
from django.http import Http404
from rest_framework import mixins, status, viewsets, permissions
from rest_framework.decorators import list_route
from rest_framework.response import Response

from realtime.models.stations import (Data, HistoricData,
                                      RadarSnapshot, Station, StationForecast, )
from realtime.serializers import (HistoricDataSerializer,
                                  RadarSnapshotSerializer,
                                  RealtimeDataSerializer,
                                  StationForecastSerializer, )


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
            data = Data.objects.filter(id__in=ids).order_by('station__name')
            serializer = RealtimeDataSerializer(
                data, many=True, context={
                    'request': request
                })
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
                data, many=False, context={
                    'request': request
                })
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
        queryset = StationForecast.objects.filter(date__gte=datetime.datetime.now).order_by('date')
        station_slug = self.request.query_params.get('station', None)
        if station_slug is not None:
            queryset = queryset.filter(station__slug=station_slug).distinct()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
