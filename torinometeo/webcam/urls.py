from django.conf.urls import patterns, url
from webcam.views import WebcamDetailView, WebcamAsyncView, WebcamIndexView

urlpatterns = patterns('webcam.views',
    url(r'^$', WebcamIndexView.as_view(), name='webcam-index'), # noqa
    url(r'^async/(?P<slug>[-\w]+)/$', WebcamAsyncView.as_view(), name='webcam-async'), # noqa
    url(r'^(?P<slug>[-\w]+)/$', WebcamDetailView.as_view(), name='webcam-detail'), # noqa
)
