from django.contrib.auth.models import User
from django.db import models

from realtime.models.stations import Station


class StationBookmark(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='utente',
        related_name='station_bookmarks',
        on_delete=models.CASCADE)
    station = models.ForeignKey(
        Station,
        verbose_name='stazione',
        related_name='bookmarks',
        on_delete=models.CASCADE)
    insertion_date = models.DateTimeField('inserimento', auto_now_add=True)

    class Meta:
        verbose_name = "Bookmark Stazione"
        verbose_name_plural = "Bookmarks Stazioni"

    def __str__(self):
        return 'stazione %s - utente %s' % (self.station.name, str(self.user))
