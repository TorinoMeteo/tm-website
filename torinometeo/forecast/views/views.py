from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.views.generic import View

from forecast.models import Forecast


class ForecastView(View):
    """ Forecast view in site
    """

    def get(self, request):
        forecast = Forecast.objects.latest('date')
        return render(request, 'forecast/view.html', {'forecast': forecast})
