from django.views.generic import View
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from forecast.models import Forecast

class ForecastView(View):
    """ Forecast view in site
    """
    def get(self, request):
        forecast = Forecast.objects.latest('date')
        return render_to_response('forecast/view.html', { 'forecast': forecast }, context_instance=RequestContext(request))
