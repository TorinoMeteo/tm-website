from django.shortcuts import render
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404

from webcam.models import Webcam

class WebcamDetailView(DetailView):
    model = Webcam
    template_name = 'webcam/detail.html'
