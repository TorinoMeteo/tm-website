from webcam.models import Webcam, BestShot

from django.contrib import admin

class WebcamBestShotInline(admin.TabularInline):
    model = BestShot
    extra = 1

class WebcamAdmin(admin.ModelAdmin):
    list_display = ['name', 'technology', 'url', ]
    prepopulated_fields = {'slug': ('name',)}
    inlines = [WebcamBestShotInline, ]

admin.site.register(Webcam, WebcamAdmin)
