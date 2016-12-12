from django.conf.urls import patterns,url
from realtime import views

urlpatterns = patterns('realtime.views',

    url(r'^jumbotron/station/(?P<id>[\d]+)/?$', views.JumbotronStationJsonView.as_view(), name='realtime-jumbotron-station-json'),
    url(r'^rete/?$', views.NetView.as_view(), name='realtime-net'),
    url(r'^entra/richiesta-inviata/?$', views.NetRequestSentView.as_view(), name='realtime-net-request-sent'),
    url(r'^entra/?$', views.NetRequestView.as_view(), name='realtime-net-request'),
    url(r'^stazione/(?P<pk>[0-9]+)/grafici/?$', views.StationIdGraphView.as_view(), name='realtime-station-graph'),
    url(r'^stazione/(?P<pk>[0-9]+)/?$', views.StationIdView.as_view(), name='realtime-station-id'),
    url(r'^(?P<slug>[A-Za-z0-9_\-]+)/live/?$', views.StationRealtimeView.as_view(), name='realtime-station-realtime'),
    url(r'^(?P<slug>[A-Za-z0-9_\-]+)/storico/$', views.StationHistoricView.as_view(), name='realtime-station-historic'),
    url(r'^(?P<slug>[A-Za-z0-9_\-]+)/grafici/dati/$', views.StationGraphJSONDataView.as_view(), name='realtime-station-graph-json-data'),
    url(r'^(?P<slug>[A-Za-z0-9_\-]+)/grafici/?$', views.StationGraphView.as_view(), name='realtime-station-graph'),
    url(r'^(?P<slug>[A-Za-z0-9_\-]+)/?$', views.StationView.as_view(), name='realtime-station'),
    url(r'^fetch/(?P<pk>[0-9]+)/?$', views.FetchView.as_view(), name='realtime-station-fetch'),

)
