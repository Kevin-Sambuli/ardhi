from django.contrib.gis.admin import GeoModelAdmin, OSMGeoAdmin
from leaflet.admin import LeafletGeoAdmin
from django.contrib.gis import admin

# Register your models here.
from .models import Parcels, ParcelDetails, Uploads


# admin.site.register(Parcels, admin.GeoModelAdmin)  # using django openlayers
# admin.site.register(Uploads, admin.GeoModelAdmin)
# admin.site.register(Parcels, admin.OSMGeoAdmin)  # using open street map
# admin.site.register(Parcels, LeafletGeoAdmin)  # using leaflet_lib
# admin.site.register(Centroids, LeafletGeoAdmin)  # using leaflet_lib

# Register your models here.
# class ParcelAdmin(LeafletGeoAdmin):
class ParcelAdmin(GeoModelAdmin):
    list_display = ('lrnumber', 'perm', 'areah', 'aream', 'owner')
    search_fields = ('gid', 'lrnumber')
    readonly_fields = ('lrnumber', 'gid', 'perm', 'areah')
    list_per_page = 10
    filter_horizontal = ()
    list_filter = ('lrnumber', 'owner')
    fieldsets = ()


# class UploadsAdmin(LeafletGeoAdmin):
class UploadsAdmin(GeoModelAdmin):
    list_display = ('lrnumber', 'plotno', 'perm', 'areah', 'aream')
    search_fields = ('gid', 'lrnumber', 'plotno')
    list_per_page = 10
    filter_horizontal = ()
    list_filter = ('lrnumber', 'plotno')
    fieldsets = ()


class ParcelDetailsAdmin(admin.ModelAdmin):
    list_display = ('parcel', 'tenure', 'encumbrances', 'land_use', 'improvements', 'status', 'registered')
    list_display_links = ('parcel',)
    list_per_page = 10
    search_fields = ('land_use', 'parcel')
    filter_horizontal = ()
    list_filter = ('tenure',)
    fieldsets = ()


# Register your models here.
admin.site.register(Parcels, ParcelAdmin)
admin.site.register(Uploads, UploadsAdmin)
admin.site.register(ParcelDetails, ParcelDetailsAdmin)
