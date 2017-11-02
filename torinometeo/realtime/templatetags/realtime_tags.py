from itertools import chain
from django import template

from realtime.models.stations import Station

register = template.Library()


@register.inclusion_tag('realtime/jumbotron.html', takes_context=True)
def realtime_jumbotron(context):
    user = context['request'].user
    if user.is_authenticated():
        ids = [b.station.id for b in user.station_bookmarks.all()]
        stations = list(chain(
            Station.objects.filter(active=True, id__in=ids),
            Station.objects.filter(active=True).exclude(id__in=ids)
        ))
    else:
        stations = Station.objects.filter(active=True)
    return {'stations': stations}


@register.inclusion_tag('realtime/widget_line.html', takes_context=True)
def realtime_line(context):
    objects = Station.objects.filter(active=True)
    stations = []
    for obj in objects:
        data = obj.get_realtime_data()
        weather = obj.weather_icon()
        print weather
        stations.append({
            'name': obj.name,
            'weather_icon': weather.get('icon') if weather else None,
            'temperature': data.temperature if data and data.temperature is not None else 'N.D.', # noqa
            'temperature_max': data.temperature_max if data and data.temperature_max is not None else 'N.D.', # noqa
            'temperature_min': data.temperature_min if data and data.temperature_min is not None else 'N.D.', # noqa
        })

    return {'stations': stations}
