from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string

from ckeditor.fields import RichTextField

from .managers import WebcamManager


def set_webcam_image_folder(instance, filename):
    """ Path to the upload folder for post images """
    return '/'.join([settings.MEDIA_WEBCAM_IMG_REL, filename])


class Webcam(models.Model):
    name = models.CharField('nome', max_length=64)
    slug = models.SlugField(max_length=128, unique=True)
    technology = models.CharField('tecnologia', max_length=128)
    description = RichTextField('descrizione', blank=True, null=True)
    url = models.URLField('url')
    web = models.URLField('pagina dedicata', blank=True, null=True)
    featured = models.BooleanField('featured', default=False)
    active = models.BooleanField('attiva', default=True)

    objects = WebcamManager()

    class Meta:
        verbose_name = 'webcam'

    def __unicode__(self):
        return '%s' % self.name

    @models.permalink
    def get_absolute_url(self):
        return ('webcam-detail', None, {
            'slug': self.slug,
        })

    def random_url(self):
        unique_id = get_random_string(length=8)
        return '%s?%s' % (self.url, unique_id)


class BestShot(models.Model):
    webcam = models.ForeignKey(Webcam, verbose_name='webcam')
    caption = models.CharField('caption', max_length=255, blank=True, null=True) # noqa
    image = models.ImageField(upload_to=set_webcam_image_folder, verbose_name='immagine') # noqa
