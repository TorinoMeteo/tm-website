from django.db import models

class StationManager(models.Manager):

    def active(self):
        return self.filter(active=True)

