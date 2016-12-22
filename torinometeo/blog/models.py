from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone

from ckeditor_uploader.fields import RichTextUploadingField

from taggit.managers import TaggableManager

""" Path to the upload folder for post images """
def set_entry_image_folder(instance, filename):
    return '/'.join([settings.MEDIA_BLOG_IMG_REL, filename])

class Entry(models.Model):

    author = models.ForeignKey(User, verbose_name='autore', related_name='entries')
    creation_date = models.DateTimeField('creazione', auto_now_add=True)
    last_edit_date = models.DateTimeField('ultima modifica', auto_now=True)
    title = models.CharField('titolo', max_length=128)
    slug = models.SlugField('slug', max_length=128)
    text = RichTextUploadingField('testo')
    image = models.ImageField('immagine', upload_to=set_entry_image_folder, blank=True, null=True)
    index_words = models.IntegerField('numero parole home')
    tags = TaggableManager('tag', help_text='valori separati da virgole', blank=True)
    published = models.BooleanField('pubblicato', default=False)
    enable_comments = models.BooleanField('abilita commenti', default=True)
    featured = models.BooleanField('featured', default=False)
    num_read = models.IntegerField('numero letture', blank=True, default=0)
    related_entries = models.ManyToManyField("self", verbose_name='articoli correlati', blank=True)

    class Meta:
        verbose_name = 'articolo'
        verbose_name_plural = 'articoli'
        ordering = ('-creation_date', )

    def __unicode__(self):
        return '%s' % self.title

    @models.permalink
    def get_absolute_url(self):
        return ('blog-detail', None, {
            'slug': self.slug,
            'year': self.creation_date.year,
            'month': self.creation_date.strftime("%m"),
            'day': self.creation_date.strftime("%d")
        })

    def get_time_attribute(self):
        return self.creation_date.strftime("%Y-%m-%dT%H:%M:%S%Z+01:00")

    def get_http_absolute_url(self):
        current_site = get_current_site(None)
        return ''.join([
            'https://' if settings.HTTPS else 'http://',
            current_site.domain,
            self.get_absolute_url()
        ])
