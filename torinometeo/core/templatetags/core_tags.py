from django import template
from django.contrib.sites.shortcuts import get_current_site
from sorl.thumbnail.templatetags.thumbnail import ThumbnailNode

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
def sharethis(relative_url, title=''):
    return {'url': relative_url, 'title': title}


def sorl_thumbnail(parser, token):
    return ThumbnailNode(parser, token)


register.tag(sorl_thumbnail)
