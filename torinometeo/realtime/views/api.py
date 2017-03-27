from django.http import Http404
from django.db.models import Max

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import list_route

from realtime.models.stations import Data
from realtime.serializers import RealtimeDataSerializer


class RealtimeDataReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """ Realtime data cRud
        Allows get realtime data
        get-last fetches only the last data
    """
    lookup_field = 'id'
    queryset = Data.objects.all()
    serializer_class = RealtimeDataSerializer

    @list_route(methods=['get'], url_path="get-last")
    def get_last(self, request, id=None, pk=None):
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
