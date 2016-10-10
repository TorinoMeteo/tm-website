from django.conf.urls import patterns,url
from webcam.views import WebcamDetailView

urlpatterns = patterns('webcam.views',
    url(r'^(?P<slug>[-\w]+)/$', WebcamDetailView.as_view(), name='webcam-detail'),
)

