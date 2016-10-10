from django import template

from realtime.models.stations import Station

register = template.Library()

@register.inclusion_tag('realtime/jumbotron.html', takes_context=True)
def realtime_jumbotron(context):
    stations = Station.objects.filter(active=True)
    return {'stations': stations}

@register.inclusion_tag('realtime/widget_line.html', takes_context=True)
def realtime_line(context):
    stations = Station.objects.filter(active=True)
    return {'stations': stations}
