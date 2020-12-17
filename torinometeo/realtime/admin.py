from django.contrib import admin
from django.utils.safestring import mark_safe

from realtime.models.geo import Nation, Province, Region
from realtime.models.stations import (Data, DataFormat, HistoricData,
                                      NetRequest, RadarColorConversion,
                                      RadarConvertParams, RadarSnapshot,
                                      Station, StationForecast, AirQualityStation, )


# geo
class NationAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'alpha2_code',
        'alpha3_code',
        'rank',
    ]


admin.site.register(Nation, NationAdmin)


class RegionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'nation',
        'rank',
    ]
    list_filter = ('nation', )


admin.site.register(Region, RegionAdmin)


class ProvinceAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'region',
        'rank',
    ]
    list_filter = ('region', )


admin.site.register(Province, ProvinceAdmin)


# stations
class StationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'nation',
        'city',
        'ranking',
        'data_format',
        'get_data_url',
        'get_webcam',
        'test_fetch',
        'test_forecast',
    ]
    list_filter = (
        'region',
        'data_format',
        'ranking',
    )
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name', )}

    fieldsets = (
        ('Denominazione/Informazioni', {
            'fields': (
                'name',
                'slug',
                'short_name',
                'description',
                'climate',
                'mean_year_rain',
                'web',
                'webcam',
                'image',
            ),
            'classes': (
                'baton-tabs-init',
                'baton-tab-fs-localization',
                'baton-tab-fs-station',
                'baton-tab-fs-data',
                'baton-tab-fs-status',
            )
        }),
        ('Localizzazione', {
            'fields': (
                'nation',
                'region',
                'province',
                'address',
                'city',
                'cap',
                'lat',
                'lng',
                'elevation',
            ),
            'classes': ('tab-fs-localization', )
        }),
        ('Stazione', {
            'fields': (
                'station_model',
                'software_model',
                'installation_type',
                'installation_position',
                'elevation_ground',
            ),
            'classes': ('tab-fs-station', )
        }),
        ('Dati', {
            'fields': (
                'data_url',
                'data_format',
                'data_date_format',
                'data_time_format',
                'forecast_url',
            ),
            'classes': ('tab-fs-data', )
        }),
        ('Stato', {
            'fields': (
                'ranking',
                'active',
            ),
            'classes': ('tab-fs-status', )
        }),
    )

    def get_data_url(self, obj):
        return mark_safe(
            '<a href="%s" target="_blank">vedi</a>' % obj.data_url)

    get_data_url.short_description = 'url dati'

    def get_webcam(self, obj):
        if not obj.webcam:
            return ''
        return mark_safe('<a href="%s" target="_blank">vedi</a>' % obj.webcam)

    get_webcam.short_description = 'webcam'

    def test_fetch(self, obj):
        return mark_safe(
            '<a href="/realtime/fetch/%d" target="_blank">test</a>' % obj.id)

    def test_forecast(self, obj):
        return mark_safe(
            '<a href="/realtime/fetchforecast/%d" target="_blank">test</a>' % obj.id)


admin.site.register(Station, StationAdmin)


class DataAdmin(admin.ModelAdmin):
    list_display = [
        'datetime',
        'station',
        'temperature',
        'temperature_max',
        'temperature_max_time',
    ]  # noqa
    list_filter = (
        'station',
        'datetime',
    )


admin.site.register(Data, DataAdmin)


class NetRequestAdmin(admin.ModelAdmin):
    list_display = [
        'date',
        'firstname',
        'lastname',
        'city',
    ]


admin.site.register(NetRequest, NetRequestAdmin)


class DataFormatAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(DataFormat, DataFormatAdmin)


class HistoricDataAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'station',
    )
    list_filter = ('station', 'date', )


admin.site.register(HistoricData, HistoricDataAdmin)


class RadarSnapshotAdmin(admin.ModelAdmin):
    list_display = (
        'filename',
        'datetime',
        'save_datetime',
        'view_image',
    )
    list_filter = ('datetime', )

    def view_image(self, obj):
        return mark_safe(
            '<a target="_blank" class="btn btn-primary" href="https://radar.torinometeo.org/images/%s">vedi</a>'  # noqa
            % obj.filename)  # noqa

    view_image.short_description = 'visualizza'


admin.site.register(RadarSnapshot, RadarSnapshotAdmin)


class RadarColorConversionAdmin(admin.ModelAdmin):
    list_display = (
        'original_color',
        'converted_color',
        'tolerance',
    )


admin.site.register(RadarColorConversion, RadarColorConversionAdmin)


class RadarConvertParamsAdmin(admin.ModelAdmin):
    list_display = (
        'param_name',
        'param_value',
    )


admin.site.register(RadarConvertParams, RadarConvertParamsAdmin)


class StationForecastAdmin(admin.ModelAdmin):
    list_display = ('date', 'period', 'station', 'icon', 'text', )
    list_filter = ('date', 'period', 'station', )


admin.site.register(StationForecast, StationForecastAdmin)


@admin.register(AirQualityStation)
class AirQualityStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'lat', 'lng', 'data', 'active', )
    list_filter = ('active', )
    search_fields = ('name', )
    autocomplete_fields = ('station', )
    prepopulated_fields = {'slug': ('name', )}

    def data(self, instance):
        return mark_safe('<a href="%s"><i class="fa fa-external-link"></i></a>' % instance.data_url)
