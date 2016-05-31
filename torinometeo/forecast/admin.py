from django.contrib import admin
from forecast.models import Forecast, DayForecast

# forecast
class DayForecastInline(admin.TabularInline):
    model = DayForecast
    extra = 1

class ForecastAdmin(admin.ModelAdmin):
    list_display = ['id', 'date',]
    inlines = [DayForecastInline, ]

admin.site.register(Forecast, ForecastAdmin)

# day forecast

class DayForecastAdmin(admin.ModelAdmin):
    list_display = ['id', 'forecast', 'date',]

admin.site.register(DayForecast, DayForecastAdmin)
