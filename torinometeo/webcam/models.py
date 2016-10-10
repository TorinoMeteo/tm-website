from django.db import models
from django.conf import settings

from ckeditor.fields import RichTextField


""" Path to the upload folder for post images """
def set_webcam_image_folder(instance, filename):
    return '/'.join([settings.MEDIA_WEBCAM_IMG_REL, filename])

class Webcam(models.Model):
    name = models.CharField('nome', max_length=64)
    slug = models.SlugField(max_length=128, unique=True)
    technology = models.CharField('tecnologia', max_length=128)
    description = RichTextField('descrizione', blank=True, null=True)
    url = models.URLField('url')
    active = models.BooleanField('attiva', default=True)

    class Meta:
        verbose_name = 'webcam'

    def __unicode__(self):
        return '%s' % self.name

    @models.permalink
    def get_absolute_url(self):
        return ('webcam-detail', None, {
            'slug': self.slug,
        })

class BestShot(models.Model):
    webcam = models.ForeignKey(Webcam, verbose_name='webcam')
    caption = models.CharField('caption', max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to=set_webcam_image_folder, verbose_name='immagine')
