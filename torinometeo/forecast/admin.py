from django.contrib import admin

from forecast.models import DayForecast, Forecast


# forecast
class DayForecastInline(admin.StackedInline):
    model = DayForecast
    extra = 1
    suit_classes = 'suit-tab suit-tab-dayforecast'


class ForecastAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'date',
        'user',
    ]
    inlines = [
        DayForecastInline,
    ]
    list_filter = ('date', )
    search_fields = ('note', )

    fieldsets = (('Principale', {
        'classes': (
            'baton-tabs-init',
            'baton-tab-inline-dayforecast_set',
        ),
        'fields': [
            'date',
            'pattern',
            'note',
        ],
    }), )

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


admin.site.register(Forecast, ForecastAdmin)

# day forecast


class DayForecastAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'forecast',
        'date',
    ]
    list_filter = ('date', )
    search_fields = ('note', )


admin.site.register(DayForecast, DayForecastAdmin)
