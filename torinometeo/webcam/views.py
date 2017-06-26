from django.shortcuts import render
from django.http import Http404
from django.views.generic import DetailView, View, ListView

from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Webcam
from .serializers import WebcamSerializer


class WebcamDetailView(DetailView):
    model = Webcam
    template_name = 'webcam/detail.html'


class WebcamAsyncView(View):
    def get(self, request, slug):
        w = Webcam.objects.get(slug=slug)
        return render(
            request,
            'webcam/async.html',
            {'webcam': w}
        )


class WebcamIndexView(ListView):
    model = Webcam

    def get_queryset(self):
        return Webcam.objects.active()


# API
class Webcams(viewsets.ViewSet):
    """ Webcams list
    """
    def list(self, request):
        """
        Gets the webcams list
        """
        data = Webcam.objects.all()
        serializer = WebcamSerializer(data, many=True,
                                      context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Gets single webcam data
        """
        try:
            webcam = Webcam.objects.get(slug=pk)
            serializer = WebcamSerializer(webcam, many=False,
                                          context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Webcam.DoesNotExist:
            raise Http404()
