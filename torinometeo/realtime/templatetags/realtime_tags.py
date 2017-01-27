from django import template

from realtime.models.stations import Station

register = template.Library()

@register.inclusion_tag('realtime/jumbotron.html', takes_context=True)
def realtime_jumbotron(context):
    stations = Station.objects.filter(active=True)
    return {'stations': stations}

@register.inclusion_tag('realtime/widget_line.html', takes_context=True)
def realtime_line(context):
    objects = Station.objects.filter(active=True)
    stations = []
    for obj in objects:
        data = obj.get_realtime_data()
        stations.append({
            'name': obj.name,
            'temperature': data.temperature if data and data.temperature is not None else 'N.D.', # noqa
            'temperature_max': data.temperature_max if data and data.temperature_max is not None else 'N.D.', # noqa
            'temperature_min': data.temperature_min if data and data.temperature_min is not None else 'N.D.', # noqa
        })

    return {'stations': stations}
