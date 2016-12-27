from django.db import models


class WebcamManager(models.Manager):
    """ Defines the active and featured methods
    """
    def active(self, **kwargs):
        return self.filter(active=True, **kwargs)

    def featured(self, **kwargs):
        return self.active(featured=True, **kwargs)
