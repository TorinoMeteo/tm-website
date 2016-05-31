from django.conf.urls import patterns,url
from forecast.views import views

urlpatterns = patterns('forecast.views',

    url(r'^/?$', views.ForecastView.as_view(), name='forecast-view'),

)
