from ardhi.regions.models import SubLocations, Locations, SubCounties, Counties
from django_filters import rest_framework as filters
from rest_framework_gis.filters import GeoFilterSet
from .models import Parcels


# from regions.models import SubLocations, Locations, SubCounties, Counties


class ParcelsFilter(GeoFilterSet):
    province = filters.CharFilter(method="get_parcel_by_sublocation", lookup_expr="within")

    class Meta:
        model = Parcels
        exclude = ["geom"]

    def get_parcel_by_sublocation(self, queryset, name, value):
        filtered_boundary = SubLocations.objects.filter(pk=value)
        if filtered_boundary:
            boundary = filtered_boundary.first()
            parcel_in_sublocation = queryset.filter(geom__within=boundary.geom)
            print('subloc', parcel_in_sublocation)
            return parcel_in_sublocation

    def get_parcel_by_location(self, queryset, name, value):
        filtered_boundary = Locations.objects.filter(pk=value)
        if filtered_boundary:
            boundary = filtered_boundary.first()
            parcel_in_location = queryset.filter(geom__within=boundary.geom)
            return parcel_in_location

    def get_parcel_by_sub_county(self, queryset, name, value):
        filtered_boundary = SubCounties.objects.filter(pk=value)
        if filtered_boundary:
            boundary = filtered_boundary.first()
            parcel_in_subcounty = queryset.filter(geom__within=boundary.geom)
            return parcel_in_subcounty

    def get_parcel_by_county(self, queryset, name, value):
        filtered_boundary = Counties.objects.filter(pk=value)
        if filtered_boundary:
            boundary = filtered_boundary.first()
            parcel_in_county = queryset.filter(geom__within=boundary.geom)
            return parcel_in_county
