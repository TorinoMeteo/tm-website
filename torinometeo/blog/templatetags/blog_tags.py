from django import template

from blog.models import Entry

import urllib, hashlib

register = template.Library()

@register.inclusion_tag('blog/featured.html')
def blog_featured():
    entries = Entry.objects.filter(featured=1)[0:2]
    return {'entries': entries}

@register.inclusion_tag('blog/archive.html')
def blog_archive():
    entries = Entry.objects.filter(published=1).order_by('-creation_date')
    return {'entries': entries}

@register.inclusion_tag('blog/tags_bar.html')
def tags_bar(tags, content_type=None):
    return {'tags': tags}
