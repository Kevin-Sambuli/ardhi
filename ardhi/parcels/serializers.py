from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers

from .models import Parcels


class ParcelSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Parcels
        fields = '__all__'
        geo_field = 'geom'