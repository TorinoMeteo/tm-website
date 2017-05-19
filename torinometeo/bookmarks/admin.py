from django.contrib import admin

from .models import StationBookmark


class StationBookmarkAdmin(admin.ModelAdmin):
    list_display = ('station', 'user', )

admin.site.register(StationBookmark, StationBookmarkAdmin)
