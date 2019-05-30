from webcam.models import Webcam, BestShot

from django.contrib import admin

class WebcamBestShotInline(admin.TabularInline):
    model = BestShot
    extra = 1

@admin.register(Webcam)
class WebcamAdmin(admin.ModelAdmin):
    list_display = ['name', 'technology', 'url', ]
    prepopulated_fields = {'slug': ('name',)}
    inlines = [WebcamBestShotInline, ]

    fieldsets = (('Principale', {
        'classes': (
            'baton-tabs-init',
            'baton-tab-inline-bestshot_set',
        ),
        'fields': [
            'name',
            'slug',
            'technology',
            'description',
            'latitude',
            'longitude',
            'url',
            'web',
            'featured',
            'active',
        ],
    }), )
