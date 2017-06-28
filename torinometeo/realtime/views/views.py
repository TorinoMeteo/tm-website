from datetime import date, datetime
import simplejson
import calendar
import logging
import random
import string


from django.shortcuts import render
from django.views.generic import View, ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView
from django.http import JsonResponse, HttpResponse
from django.http import Http404
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from sorl.thumbnail import get_thumbnail

from realtime.models.stations import Station
from realtime.forms import NetRequestForm
from realtime.fetch.shortcuts import fetch_data

# Get an instance of a logger
logger = logging.getLogger(__name__)


def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))


class JumbotronStationJsonView(View):
    """ Json used in jumbotron component
    """
    def get(self, request, id):
        data = {}

        try:
            station = Station.objects.get(pk=id)
        except Station.DoesNotExist:
            station = None

        if station:

            realtime_data = station.get_realtime_data()
            day_data = station.get_last24_data()

            image_url = station.image.url
            bookmarked = station.bookmarks.filter(user=request.user).exists() if request.user.is_authenticated() else False # noqa

            data['id'] = station.id
            data['name'] = station.name
            data['bookmarked'] = bookmarked
            data['authenticated'] = request.user.is_authenticated()
            data['nation'] = station.nation.name
            data['region'] = station.region.name
            data['province'] = station.province.name if station.province else '' # noqa
            data['image_url'] = image_url
            data['day_data'] = day_data
            if realtime_data:
                data['data_date'] = realtime_data.datetime.strftime("%d/%m/%Y %H:%M") # noqa
                data['data'] = {
                    'temperature': realtime_data.temperature,
                    'pressure': realtime_data.pressure,
                    'relative_humidity': realtime_data.relative_humidity,
                    'wind_strength': realtime_data.wind_strength,
                    'wind_dir': realtime_data.wind_dir,
                    'wind_dir_text': realtime_data.wind_dir_text,
                    'rain_rate': realtime_data.rain_rate,
                    'rain': realtime_data.rain,
                }

        return JsonResponse(data)


class NetView(ListView):
    """ List of all weather stations
    """
    model = Station
    queryset = Station.objects.active().order_by('name')
    template_name = 'realtime/net.html'


class StationView(DetailView):
    """ Station detail view
        main view
    """
    model = Station
    template_name = 'realtime/station.html'


class StationIdView(DetailView):
    """ Station detail view
        main view
        @TODO remove when the new map is developed with the right slug
              and so the StationView class can be used
    """
    model = Station
    template_name = 'realtime/station.html'


class StationRealtimeView(DetailView):
    """ Station detail view
        realtime view
    """
    model = Station
    template_name = 'realtime/station_realtime.html'

    def get_context_data(self, **kwargs):
        context = super(StationRealtimeView, self).get_context_data(**kwargs)
        realtime_data = context['object'].get_realtime_data()
        if realtime_data is not None:
            context['data'] = realtime_data
            context['data_date'] = realtime_data.datetime.strftime("%d/%m/%Y %H:%M") # noqa
        else:
            context['data'] = None
            context['data_date'] = None
            context['offline_limit'] = Station.RT_RANGE_SECONDS

        day_data = context['object'].get_day_data()

        context['day_data'] = simplejson.dumps(day_data)

        return context


class StationHistoricView(DetailView):
    """ Station detail view
        historic view
    """
    model = Station
    template_name = 'realtime/station_historic.html'

    def get_context_data(self, **kwargs): # noqa
        # Call the base implementation first to get a context
        context = super(StationHistoricView, self).get_context_data(**kwargs)

        m = int(self.request.GET.get('m') or 0)
        y = int(self.request.GET.get('y') or 0)

        today = date.today()
        context['today'] = today

        first_date = context['object'].get_data_first_date()
        context['first_date'] = first_date
        context['min_year'] = first_date.year
        context['min_month'] = first_date.month
        context['range_years'] = [context['min_year'] + i for i in range(int(today.year + 1) - context['min_year'])] # noqa

        if(m > 0 and m < 13 and y >= first_date.year and y <= today.year):
            context['month'] = m
            context['year'] = y
            first_month_day = date(y, m, 1)
            last_day_month = calendar.monthrange(y, m)[1]
            d = date(y, m, last_day_month)

        else:
            first_month_day = date(today.year, today.month, 1)
            context['month'] = int(first_month_day.strftime('%m'))
            context['year'] = int(first_month_day.strftime('%Y'))
            last_day_month = today.day
            d = today

        context['data'] = context['object'].get_historic_data(first_month_day, d) # noqa

        first_1d = True
        t_mean_max_1d = 0
        t_mean_min_1d = 0
        t_mean_mean_1d = 0
        t_min_1d = 0
        t_max_1d = 0
        p_min_1d = 0
        p_max_1d = 0
        rh_min_1d = 0
        rh_max_1d = 0
        r_sum_1d = 0

        first_2d = True
        t_mean_max_2d = 0
        t_mean_min_2d = 0
        t_mean_mean_2d = 0
        t_min_2d = 0
        t_max_2d = 0
        p_min_2d = 0
        p_max_2d = 0
        rh_min_2d = 0
        rh_max_2d = 0
        r_sum_2d = 0

        first_3d = True
        t_mean_max_3d = 0
        t_mean_min_3d = 0
        t_mean_mean_3d = 0
        t_min_3d = 0
        t_max_3d = 0
        p_min_3d = 0
        p_max_3d = 0
        rh_min_3d = 0
        rh_max_3d = 0
        r_sum_3d = 0

        first_m = True
        t_mean_max_m = 0
        t_mean_min_m = 0
        t_mean_mean_m = 0
        t_min_m = 0
        t_max_m = 0
        p_min_m = 0
        p_max_m = 0
        rh_min_m = 0
        rh_max_m = 0
        r_sum_m = 0

        range_1d = 0
        range_2d = 0
        range_3d = 0
        range_m = 0

        for d in context['data']:
            if d.get('temperature_max') is not None:
                range_m += 1
                t_mean_max_m = t_mean_max_m + d.get('temperature_max')
                t_mean_min_m = t_mean_min_m + d.get('temperature_min')
                t_mean_mean_m = t_mean_mean_m + d.get('temperature_mean')

                if first_m or t_min_m > d.get('temperature_min'):
                    t_min_m = d.get('temperature_min')
                if first_m or t_max_m < d.get('temperature_max'):
                    t_max_m = d.get('temperature_max')

                if first_m or p_min_m > d.get('pressure_min'):
                    p_min_m = d.get('pressure_min')
                if first_m or p_max_m < d.get('pressure_max'):
                    p_max_m = d.get('pressure_max')

                if first_m or rh_min_m > d.get('relative_humidity_min'):
                    rh_min_m = d.get('relative_humidity_min')
                if first_m or rh_max_m < d.get('relative_humidity_max'):
                    rh_max_m = d.get('relative_humidity_max')

                r_sum_m = r_sum_m + d.get('rain')

                first_m = False

                if d.get('date_obj').day <= 10:
                    range_1d += 1
                    t_mean_max_1d = t_mean_max_1d + d.get('temperature_max')
                    t_mean_min_1d = t_mean_min_1d + d.get('temperature_min')
                    t_mean_mean_1d = t_mean_mean_1d + d.get('temperature_mean')

                    if first_1d or t_min_1d > d.get('temperature_min'):
                        t_min_1d = d.get('temperature_min')
                    if first_1d or t_max_1d < d.get('temperature_max'):
                        t_max_1d = d.get('temperature_max')

                    if first_1d or p_min_1d > d.get('pressure_min'):
                        p_min_1d = d.get('pressure_min')
                    if first_1d or p_max_1d < d.get('pressure_max'):
                        p_max_1d = d.get('pressure_max')

                    if first_1d or rh_min_1d > d.get('relative_humidity_min'):
                        rh_min_1d = d.get('relative_humidity_min')
                    if first_1d or rh_max_1d < d.get('relative_humidity_max'):
                        rh_max_1d = d.get('relative_humidity_max')

                    r_sum_1d = r_sum_1d + d.get('rain')

                    first_1d = False

                elif d.get('date_obj').day <= 20:
                    range_2d += 1
                    t_mean_max_2d = t_mean_max_2d + d.get('temperature_max')
                    t_mean_min_2d = t_mean_min_2d + d.get('temperature_min')
                    t_mean_mean_2d = t_mean_mean_2d + d.get('temperature_mean')

                    if first_2d or t_min_2d > d.get('temperature_min'):
                        t_min_2d = d.get('temperature_min')
                    if first_2d or t_max_2d < d.get('temperature_max'):
                        t_max_2d = d.get('temperature_max')

                    if first_2d or p_min_2d > d.get('pressure_min'):
                        p_min_2d = d.get('pressure_min')
                    if first_2d or p_max_2d < d.get('pressure_max'):
                        p_max_2d = d.get('pressure_max')

                    if first_2d or rh_min_2d > d.get('relative_humidity_min'):
                        rh_min_2d = d.get('relative_humidity_min')
                    if first_2d or rh_max_2d < d.get('relative_humidity_max'):
                        rh_max_2d = d.get('relative_humidity_max')

                    r_sum_2d = r_sum_2d + d.get('rain')

                    first_2d = False

                elif d.get('date_obj').day <= last_day_month:
                    range_3d += 1
                    t_mean_max_3d = t_mean_max_3d + d.get('temperature_max')
                    t_mean_min_3d = t_mean_min_3d + d.get('temperature_min')
                    t_mean_mean_3d = t_mean_mean_3d + d.get('temperature_mean')

                    if first_3d or t_min_3d > d.get('temperature_min'):
                        t_min_3d = d.get('temperature_min')
                    if first_3d or t_max_3d < d.get('temperature_max'):
                        t_max_3d = d.get('temperature_max')

                    if first_3d or p_min_3d > d.get('pressure_min'):
                        p_min_3d = d.get('pressure_min')
                    if first_3d or p_max_3d < d.get('pressure_max'):
                        p_max_3d = d.get('pressure_max')

                    if first_3d or rh_min_3d > d.get('relative_humidity_min'):
                        rh_min_3d = d.get('relative_humidity_min')
                    if first_3d or rh_max_3d < d.get('relative_humidity_max'):
                        rh_max_3d = d.get('relative_humidity_max')

                    r_sum_3d = r_sum_3d + d.get('rain')

                    first_3d = False

        context['last_day_month'] = last_day_month

        context['t_mean_max_1d'] = round(t_mean_max_1d/range_1d, 2)
        context['t_mean_min_1d'] = round(t_mean_min_1d/range_1d, 2)
        context['t_mean_mean_1d'] = round(t_mean_mean_1d/range_1d, 2)
        context['t_min_1d'] = t_min_1d
        context['t_max_1d'] = t_max_1d
        context['p_min_1d'] = p_min_1d
        context['p_max_1d'] = p_max_1d
        context['rh_min_1d'] = rh_min_1d
        context['rh_max_1d'] = rh_max_1d
        context['r_sum_1d'] = r_sum_1d

        context['t_mean_max_2d'] = round(t_mean_max_2d/range_2d, 2)
        context['t_mean_min_2d'] = round(t_mean_min_2d/range_2d, 2)
        context['t_mean_mean_2d'] = round(t_mean_mean_2d/range_2d, 2)
        context['t_min_2d'] = t_min_2d
        context['t_max_2d'] = t_max_2d
        context['p_min_2d'] = p_min_2d
        context['p_max_2d'] = p_max_2d
        context['rh_min_2d'] = rh_min_2d
        context['rh_max_2d'] = rh_max_2d
        context['r_sum_2d'] = r_sum_2d

        context['t_mean_max_3d'] = round(t_mean_max_3d/range_3d, 2)
        context['t_mean_min_3d'] = round(t_mean_min_3d/range_3d, 2)
        context['t_mean_mean_3d'] = round(t_mean_mean_3d/range_3d, 2)
        context['t_min_3d'] = t_min_3d
        context['t_max_3d'] = t_max_3d
        context['p_min_3d'] = p_min_3d
        context['p_max_3d'] = p_max_3d
        context['rh_min_3d'] = rh_min_3d
        context['rh_max_3d'] = rh_max_3d
        context['r_sum_3d'] = r_sum_3d

        context['t_mean_max_m'] = round(t_mean_max_m/range_m, 2)
        context['t_mean_min_m'] = round(t_mean_min_m/range_m, 2)
        context['t_mean_mean_m'] = round(t_mean_mean_m/range_m, 2)
        context['t_min_m'] = t_min_m
        context['t_max_m'] = t_max_m
        context['p_min_m'] = p_min_m
        context['p_max_m'] = p_max_m
        context['rh_min_m'] = rh_min_m
        context['rh_max_m'] = rh_max_m
        context['r_sum_m'] = r_sum_m

        return context


class StationGraphView(DetailView):
    """ Station detail view
        graphs view
    """
    model = Station
    template_name = 'realtime/station_graph.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(StationGraphView, self).get_context_data(**kwargs)
        today = date.today()
        first_month_day = date(today.year, today.month, 1)
        context['to_date'] = today.strftime('%d/%m/%Y')
        context['from_date'] = first_month_day.strftime('%d/%m/%Y')
        return context


class StationIdGraphView(DetailView):
    """ Station detail view
        graphs view
        @TODO remove when the new map is developed with the right slug
              and so the StationGraphView class can be used
    """
    model = Station
    template_name = 'realtime/station_graph.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(StationGraphView, self).get_context_data(**kwargs)
        today = date.today()
        first_month_day = date(today.year, today.month, 1)
        context['to_date'] = today.strftime('%d/%m/%Y')
        context['from_date'] = first_month_day.strftime('%d/%m/%Y')
        return context


class StationGraphJSONDataView(View):
    """ Historical data JSON
        called by ajax
    """
    def get(self, request, slug):
        data = {}

        try:
            station = Station.objects.get(slug=slug)
        except Station.DoesNotExist:
            station = None

        if station:
            from_date = datetime.strptime(request.GET['from_date'], '%d/%m/%Y')
            to_date = datetime.strptime(request.GET['to_date'], '%d/%m/%Y')
            data = station.get_historic_data(from_date, to_date)

        return JsonResponse(data, safe=False)


class NetRequestView(CreateView):
    """ Net entrance request form view
    """
    template_name = 'realtime/net_request.html'
    form_class = NetRequestForm
    success_url = reverse_lazy('realtime-net-request-sent')

    def form_valid(self, form):
        form.send_request_mail()
        return super(NetRequestView, self).form_valid(form)


class NetRequestSentView(TemplateView):
    """ Net entrance request sent view
    """
    template_name = 'realtime/net_request_sent.html'


class FetchView(View):

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(FetchView, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        station = Station.objects.get(pk=pk)

        data = fetch_data(
            station.data_url,
            station.data_format.name,
            time_format=station.data_time_format.split(','),
            date_format=station.data_date_format.split(','),
        )
        json_data = data.as_json()

        return render(
            request,
            'realtime/fetch.html',
            {'station': station, 'data': data, 'json_data': json_data}
        )


class WebcamView(View):
    def get(self, request, pk):
        station = Station.objects.get(pk=pk)
        if station.webcam:
            url = station.webcam + '?' + randomword(10)
            im = get_thumbnail(url, '800', quality=50) # noqa
            return HttpResponse(im.read(), content_type="image/jpg")
        else:
            raise Http404("Station does not have a webcam associated")
