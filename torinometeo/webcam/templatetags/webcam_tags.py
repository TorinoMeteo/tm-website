from django import template

from ..models import Webcam

register = template.Library()


@register.inclusion_tag('webcam/widget.html', takes_context=True)
def webcam_widget(context):
    webcams = Webcam.objects.featured()
    return {'webcams': webcams}
