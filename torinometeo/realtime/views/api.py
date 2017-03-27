from django.http import Http404
from django.db.models import Max

from rest_framework import viewsets, status
from rest_framework.response import Response

from realtime.models.stations import Data
from realtime.serializers import RealtimeDataSerializer


class LastRealtimeData(viewsets.ViewSet):
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
            data = Data.objects.filter(id__in=ids)
            serializer = RealtimeDataSerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Data.DoesNotExist:
            raise Http404()
