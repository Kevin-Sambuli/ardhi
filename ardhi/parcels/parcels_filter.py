from rest_framework_gis.filterset import GeoFilterSet
from django_filters import filters
from .models import Parcels
from ardhi.regions.models import SubLocations


class ParcelFilter(GeoFilterSet):
    sub_county = filters.CharFilter(method='get_facilities_by_sub_location',  lookup_expr="within"
    )

    class Meta:
        model = Parcels
        exclude = ['geom']

    def get_facilities_by_sub_location(self, queryset, name, value):
        filtered_boundary = SubLocations.objects.filter(pk=value)
        if filtered_boundary:
            boundary = filtered_boundary.first()
            hospitals_in_province = queryset.filter(geom__within=boundary.mpoly)
            return hospitals_in_province
#         return queryset
