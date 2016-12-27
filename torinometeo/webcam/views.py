from django.shortcuts import render
from django.views.generic import DetailView, View, ListView
# from django.shortcuts import get_object_or_404

from .models import Webcam


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
