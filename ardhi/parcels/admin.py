# from django.contrib.gis.admin import GeoModelAdmin, OSMGeoAdmin
from django.contrib.gis import admin
# from django.contrib.gis.admin import OSMGeoAdmin
from leaflet.admin import LeafletGeoAdmin


# Register your models here.
from .models import Parcels, ParcelDetails

# admin.site.register(Parcels, admin.GeoModelAdmin)  # using django openlayers
# admin.site.register(Parcels, admin.OSMGeoAdmin)  # using open street map
# admin.site.register(Parcels, LeafletGeoAdmin)  # using leaflet_lib
# admin.site.register(Centroids, LeafletGeoAdmin)  # using leaflet_lib


# Register your models here.


class ParcelAdmin(LeafletGeoAdmin):
    list_display = ('lr_no', 'id', 'perimeter', 'area_ha', 'owner')
    search_fields = ('id', 'lr_no')
    readonly_fields = ('lr_no', 'id', 'perimeter', 'area_ha') #,'owner')
    list_per_page = 10
    filter_horizontal = ()
    list_filter = ('lr_no', 'owner')
    fieldsets = ()


class ParcelDetailsAdmin(admin.ModelAdmin):
    list_display = ('parcel', 'tenure', 'encumbrances', 'land_use', 'improvements', 'registered')
    list_display_links = ('parcel',)
    list_per_page = 10
    # readonly_fields = ('parcel', 'tenure', 'encumbrances', 'land_use', 'improvements', 'registered')
    search_fields = ('land_use', 'parcel')
    filter_horizontal = ()
    list_filter = ('tenure',)
    fieldsets = ()


# Register your models here.
admin.site.register(Parcels, ParcelAdmin)
admin.site.register(ParcelDetails, ParcelDetailsAdmin)

