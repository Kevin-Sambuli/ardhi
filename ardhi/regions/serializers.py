from rest_framework_gis.serializers import GeoFeatureModelSerializer
# from rest_framework import serializers

from .models import Counties, SubCounties, Locations, SubLocations


class CountiesSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Counties
        fields = '__all__'
        geo_field = 'geom'


class SUbCountiesSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = SubCounties
        fields = '__all__'
        geo_field = 'geom'


class LocationSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Locations
        fields = '__all__'
        geo_field = 'geom'


class SUbLocationSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = SubLocations
        fields = '__all__'
        geo_field = 'geom'

