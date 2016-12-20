from django.db import models


class StationManager(models.Manager):
    """ Defines the active method to easily retrieve active stations
    """
    def active(self, **kwargs):
        return self.filter(active=True, **kwargs)
