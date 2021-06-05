# from django.contrib.gis.admin import GeoModelAdmin, OSMGeoAdmin
from django.contrib.gis import admin
# from django.contrib.gis.admin import OSMGeoAdmin
from leaflet.admin import LeafletGeoAdmin

# Register your models here.
from .models import Counties, SubCounties, SubLocations, Locations


admin.site.register(Counties, admin.GeoModelAdmin)  # using django openlayers
admin.site.register(SubCounties, admin.OSMGeoAdmin)  # using open street map
admin.site.register(Locations, LeafletGeoAdmin)  # using leaflet_lib
admin.site.register(SubLocations, LeafletGeoAdmin)  # using leaflet_lib


# Register your models here.
class CountiesAdmin(LeafletGeoAdmin):
    list_display = ('id', 'coucode', 'first_coun')
    list_display_links = ('first_coun',)
    search_fields = ('coucode', 'first_coun')
    readonly_fields = ('id', 'coucode', 'first_coun')
    list_per_page = 10
    filter_horizontal = ()
    list_filter = ('first_coun',)
    fieldsets = ()


class SubCountyAdmin(LeafletGeoAdmin):
    list_display = ('id', 'sccodefull', 'first_scou')
    list_display_links = ('first_scou',)
    list_per_page = 10
    readonly_fields = ('id', 'sccodefull', 'first_scou')
    search_fields = ('sccodefull', 'first_scou')
    filter_horizontal = ()
    # list_filter = ('first_scou',)
    fieldsets = ()


class LocationAdmin(LeafletGeoAdmin):
    list_display = ('id', 'loccodeful', 'first_locn')
    list_display_links = ('first_locn',)
    list_per_page = 10
    readonly_fields = ('loccodeful', 'first_locn')
    search_fields = ('loccodeful', 'first_locn',)
    filter_horizontal = ()
    # list_filter = ('first_locn',)
    fieldsets = ()


class SubLocationAdmin(LeafletGeoAdmin):
    list_display = ('id','slcodefull', 'first_slna')
    list_display_links = ('first_slna',)
    list_per_page = 10
    readonly_fields = ('slcodefull', 'first_slna')
    search_fields = ('slcodefull', 'first_slna')
    filter_horizontal = ()
    # list_filter = ('first_slna',)
    fieldsets = ()


# Register your models here.
# admin.site.register(Counties, CountiesAdmin)
# admin.site.register(SubCounties, SubCountyAdmin)
# admin.site.register(Locations, LocationAdmin)
# admin.site.register(SubLocations, SubLocationAdmin)
