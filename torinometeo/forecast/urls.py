from django.conf.urls import url
from forecast.views import views

urlpatterns = [
    url(r'^/?$', views.ForecastView.as_view(), name='forecast-view'),
]
