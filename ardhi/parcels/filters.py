# from ardhi.regions.models import SubLocations, Locations, SubCounties, Counties
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


# SELECT jsonb_build_object FROM public."parcelView";
# query1 = ('SELECT jsonb_build_object FROM public.parcels_geojson;')


# cur.execute(query1)
#
# parcels = cur.fetchall()
# parcels = parcels[0][0]

      # SELECT jsonb_build_object FROM public."parcelView";
        # query1 = ('SELECT jsonb_build_object FROM public.parcelView;')

def parcelJson():
    return """
        SELECT jsonb_build_object(
            'type','FeatureCollection',
            'features', jsonb_agg(features.feature)
            )
              FROM ( 
                  SELECT jsonb_build_object( 
                  'type','Feature',
                  'geometry', ST_AsGeoJSON(geom)::jsonb,
                  'properties',to_jsonb(inputs)  -'geom') 
              AS feature, 'geometry' 
              FROM (
              SELECT * FROM nairobi
              ) inputs
            ) features;
        """


def myParcels(table=None, owner_id=None):
    """ Create a quuery that returns GeoJSON data from parcels data in PostGIS.
        """
    # TODO: ensure this query is secured from SQL injection
    # by using a psycopg2 parameterized query

    # TODO: determine how best to allow WHERE clause
    # to filter based on fclass and possibly geometry.
    return f"""
            SELECT jsonb_build_object(
                'type','FeatureCollection',
                'features', jsonb_agg(features.feature)
            )
            FROM ( 
                SELECT jsonb_build_object( 
                    'type','Feature',
                    'geometry', ST_AsGeoJSON(geom)::jsonb,
                    'properties',  to_jsonb(inputs)  -'geom'
                ) 
                AS feature, 'geometry' 
                    FROM (
                        SELECT * FROM {table} 
                            where owner_id ={owner_id}
                        ) inputs
                    ) features;
                """


def create_osm_to_geojson_query(table=None, fclass=None, limit=10, xmin=23.5, ymin=61.45, xmax=23.8, ymax=61.5,
                                epsg=4326, ):
    """
    Create a quuery that returns GeoJSON data from OSM data in PostGIS.
    """
    # TODO: ensure this query is secured from SQL injection
    # by using a psycopg2 parameterized query

    # TODO: determine how best to allow WHERE clause
    # to filter based on fclass and possibly geometry.
    return f"""
        SELECT jsonb_build_object(
            'type',     'FeatureCollection',
            'features', jsonb_agg(feature)
        )
        FROM (
            SELECT jsonb_build_object(
                'type',       'Feature',
                'id',         osm_id,
                'geometry',   ST_AsGeoJSON(geometry)::jsonb,
                'properties', to_jsonb(inputs) - 'geometry'
            ) AS feature
            FROM (
                SELECT 
                    "osm_id",
                    "code",
                    "fclass",
                    "name",
                    "geometry"
                FROM {table}
                -- where bounding box contains geometry
                -- https://postgis.net/docs/ST_Geometry_Contain.html
                WHERE ST_MakeEnvelope (
                    {xmin}, {ymin},
                    {xmax}, {ymax},
                    {epsg}
                ) ~ "geometry"
                AND "fclass" = 'supermarket'
                --limit {limit}
            ) inputs
        ) features;
    """
