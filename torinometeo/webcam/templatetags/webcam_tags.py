from django import template

from webcam.models import Webcam

register = template.Library()

@register.inclusion_tag('webcam/widget.html', takes_context=True)
def webcam_widget(context):
    webcams = Webcam.objects.filter(active=True)
    return {'webcams': webcams}
