from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('social_auth/signin_btn.html', takes_context=True)
def social_auth_signin_btn(context):
    return {'request': context['request'], 'profile_url': getattr(settings, 'PROFILE_URL', None)}
