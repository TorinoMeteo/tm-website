import datetime

from django.http import Http404
from django.db.models import Max

from rest_framework import viewsets, status, mixins
from rest_framework.response import Response

from realtime.models.stations import Station, Data, HistoricData
from realtime.serializers import RealtimeDataSerializer, HistoricDataSerializer


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
            serializer = RealtimeDataSerializer(data, many=True,
                                                context={'request': request})
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
            serializer = RealtimeDataSerializer(data, many=False,
                                                context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Station.DoesNotExist:
            raise Http404()


class HistoricDataViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
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
                day=int(self.kwargs['day'])
            )
        except:
            date = datetime.date.fromordinal(datetime.date.today().toordinal() - 1) # noqa

        return HistoricData.objects.filter(date=date).order_by('station__name')
