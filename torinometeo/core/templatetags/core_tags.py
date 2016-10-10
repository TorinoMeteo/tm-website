from django import template
from django.contrib.sites.models import get_current_site

register = template.Library()


@register.filter()
def strip_img(html):
    import re
    TAG_RE = re.compile(r'<img.+?/>')
    return TAG_RE.sub('', html)


@register.filter()
def absurl(url):
    request = None
    return ''.join(['http://', get_current_site(request).domain, str(url)])


@register.inclusion_tag('core/sharethis.html')
def sharethis(relative_url):
    return {'url': relative_url}
