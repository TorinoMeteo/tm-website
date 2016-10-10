from django.contrib import admin
from realtime.models.geo import Nation, Region, Province
from realtime.models.stations import Station, Data, NetRequest

# geo

class NationAdmin(admin.ModelAdmin):
    list_display = ['name', 'alpha2_code', 'alpha3_code', 'rank',]

admin.site.register(Nation, NationAdmin)

class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'nation', 'rank',]
    list_filter = ('nation', )

admin.site.register(Region, RegionAdmin)

class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['name', 'region', 'rank',]
    list_filter = ('region', )

admin.site.register(Province, ProvinceAdmin)

# stations

class StationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'nation', 'region', 'province', 'city', 'data_url', 'webcam',]
    list_filter = ('region', )

    fieldsets = (
        ('Denominazione/Informazioni', {
            'fields': ('name', 'slug', 'short_name', 'description', 'climate', 'mean_year_rain', 'web', 'webcam', 'image',)
        }),
        ('Localizzazione', {
            'fields': ('nation', 'region', 'province', 'address', 'city', 'cap', 'lat', 'lng', 'elevation',)
        }),
        ('Stazione', {
            'fields': ('station_model', 'software_model', 'installation_type', 'installation_position', 'elevation_ground', 'cap', 'lat', 'lng', 'elevation',)
        }),
        ('Dati', {
            'fields': ('data_url', 'data_type', 'data_date_regexp', 'data_time_regexp', 'forecast_url',)
        }),
        ('Stato', {
            'fields': ('active',)
        }),
    )

admin.site.register(Station, StationAdmin)

class DataAdmin(admin.ModelAdmin):
    list_display = ['datetime', 'station', 'temperature',]
    list_filter = ('station', 'datetime', )

admin.site.register(Data, DataAdmin)

class NetRequestAdmin(admin.ModelAdmin):
    list_display = ['date', 'firstname', 'lastname', 'city',]

admin.site.register(NetRequest, NetRequestAdmin)
