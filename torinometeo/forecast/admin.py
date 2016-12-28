from django.contrib import admin
from forecast.models import Forecast, DayForecast

# forecast
class DayForecastInline(admin.StackedInline):
    model = DayForecast
    extra = 1
    suit_classes = 'suit-tab suit-tab-dayforecast'

class ForecastAdmin(admin.ModelAdmin):
    list_display = ['id', 'date',]
    inlines = [DayForecastInline, ]

    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-main',),
            'fields': ['date', 'pattern', ],
        }),
    )

    suit_form_tabs = (
        ('main', 'Principale'),
        ('dayforecast', 'Previsioni giornate'),
    )

admin.site.register(Forecast, ForecastAdmin)

# day forecast

class DayForecastAdmin(admin.ModelAdmin):
    list_display = ['id', 'forecast', 'date',]

admin.site.register(DayForecast, DayForecastAdmin)
