from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers

from .models import Parcels
from ardhi.regions.models import SubLocations


class SubLocationSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = SubLocations
        fields = '__all__'
        geo_field = 'geom'


class ParcelSerializer(GeoFeatureModelSerializer):
    distance = serializers.CharField()

    class Meta:
        model = Parcels
        fields = '__all__'
        geo_field = 'geom'
        # read_only_fields = ['distance']
