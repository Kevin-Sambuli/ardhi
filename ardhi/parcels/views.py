import json

from django import forms
from django.http import JsonResponse, HttpResponse
from django.core.serializers import serialize
from djgeojson.views import GeoJSONLayerView

from .models import Parcels, ParcelDetails
from .map import my_map
from .database import get_cursor

from django.shortcuts import render, get_object_or_404
from .utils import get_geo, get_center_coordinates, get_zoom
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium


# from .forms import MeasurementModelForm


def parcels(request):
    user = request.user.id_no
    # owner = Parcels.objects.filter(owner_id=user.id).value_list('lr_no')
    print('details', ParcelDetails.objects.get(parcel__id=84))
    print('email', user)
    tree = ParcelDetails.objects.get(parcel__id=84)
    print(tree.land_use)
    # user = request.user print(user.id, user.username)
    # print('my parcels',Parcels.objects.filter(owner_id=user.id))
    # all_commenter_ids = PhotoComment.objects.filter(which_photo=which_photo).order_by('-id').values_list(
    # 'submitted_by', flat=True)[:25]
    points_as_geojson = serialize('geojson', Parcels.objects.all())
    parcel = serialize('geojson', Parcels.objects.filter(owner_id=request.user.id))
    # map2 = my_map(parcel=parcel, land_parcels=points_as_geojson)
    # map2.save('templates/parcels/my_map.html')

    print('parcels', parcel)
    print('land parcels', Parcels.objects.all())

    print(points_as_geojson)
    return HttpResponse(points_as_geojson, content_type='json')
    # return JsonResponse(json.loads(points_as_geojson))


# from django.contrib.gis.geos import Point
# from django.contrib.gis.measure import D
# from django.db.models import Sum
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import status, viewsets
# from rest_framework.decorators import action
# from rest_framework.response import Response
#
# from .filters import HospitalsFilter
# from .models import Hospital
# from .serializers import HospitalSerializer
#
#
# class HospitalViewSet(viewsets.ModelViewSet):
#     queryset = Hospital.objects.all()
#     serializer_class = HospitalSerializer
#     filter_class = HospitalsFilter
#     filter_backends = (DjangoFilterBackend,)
#
#     @action(detail=False, methods=["get"])
#     def total_bed_capacity(self, request):
#         bed_capacity = Hospital.objects.aggregate(bed_capacity=Sum("beds"))
#         return Response(bed_capacity)
#
#     @action(detail=False, methods=["get"])
#     def province_beds_capacity(self, request):
#         province_bed_capacity = Hospital.objects.values("province_name").annotate(
#             bed_capacity=Sum("beds")
#         )
#         return Response(province_bed_capacity)
#
#     @action(detail=False, methods=["get"])
#     def closest_hospitals(self, request):
#         """Get Hospitals that are at least 3km or less from a users location"""
#         longitude = request.GET.get("lon", None)
#         latitude = request.GET.get("lat", None)
#
#         if longitude and latitude:
#             user_location = Point(float(longitude), float(latitude), srid=4326)
#             closest_hospitals = Hospital.objects.filter(
#                 geom__distance_lte=(user_location, D(km=3))
#             )
#             serializer = self.get_serializer_class()
#             serialized_hospitals = serializer(closest_hospitals, many=True)
#             return Response(serialized_hospitals.data, status=status.HTTP_200_OK)
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# class ParcelGeoJson(GeoJSONLayerView):
#     model = Parcels
#     properties = ('popup_content',)
#
#
# def parcel_js(request):
#     parcel = Parcels.objects.all()
#     context = {'object_list': parcel,}
#     return render(request, 'poco/poco_js.html', context)


def get_points(request):
    cur = get_cursor()
    # cur.execute("""SELECT json_build_object('type', 'Feature','geometry', ST_AsGeoJSON(the_geom :: geometry) :: json,
    # 'properties', json_build_object('name', name)) jsonb FROM parcels;""")

    # queryset_parcels = ("""SELECT jsonb_build_object('type','FeatureCollection','features', jsonb_agg(features.feature))
    #        FROM ( SELECT jsonb_build_object( 'type','Feature','geometry', ST_AsGeoJSON(geom)::jsonb,'properties',
    #        to_jsonb(inputs)  -'geom') AS feature, 'geometry'
    #        FROM (SELECT * FROM parcels) inputs) features;""")

    query1 = ('SELECT jsonb_build_object FROM public.parcels_json;')
    cur.execute(query1)

    # query_set_centroids = ("""SELECT jsonb_build_object('type','FeatureCollection','features', jsonb_agg(
    # features.feature)) FROM ( SELECT jsonb_build_object( 'type','Feature','geometry', ST_AsGeoJSON(ST_Centroid(
    # geom))::jsonb,'properties',  to_jsonb(inputs)  -'geom') AS feature, 'geometry' FROM (SELECT * FROM parcels)
    # inputs) features;""")

    query2 = ('SELECT jsonb_build_object FROM public.centroids_json;')
    cur.execute(query2)

    parcel = cur.fetchall()
    centroids_json = parcel[0][0]
    print('parcel', parcel)
    print('centroids', centroids_json)
    return JsonResponse(centroids_json)

# def calculate_distance_view(request):
#     # initial values
#     distance = None
#     destination = None
#
#     obj = get_object_or_404(Parcels, id=1)
#     form = MeasurementModelForm(request.POST or None)
#     geolocator = Nominatim(user_agent='measurements')
#
#     ip = '72.14.207.99'
#     country, city, lat, lon = get_geo(ip)
#     location = geolocator.geocode(city)
#
#     # location coordinates
#     l_lat = lat
#     l_lon = lon
#     pointA = (l_lat, l_lon)
#
#     # initial folium map
#     m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon), zoom_start=8)
#     # location marker
#     folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=city['city'],
#                   icon=folium.Icon(color='purple')).add_to(m)
#
#     if form.is_valid():
#         instance = form.save(commit=False)
#         destination_ = form.cleaned_data.get('destination')
#         destination = geolocator.geocode(destination_)
#
#         # destination coordinates
#         d_lat = destination.latitude
#         d_lon = destination.longitude
#         pointB = (d_lat, d_lon)
#         # distance calculation
#         distance = round(geodesic(pointA, pointB).km, 2)
#
#         # folium map modification
#         m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon, d_lat, d_lon),
#                        zoom_start=get_zoom(distance))
#         # location marker
#         folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=city['city'],
#                       icon=folium.Icon(color='purple')).add_to(m)
#         # destination marker
#         folium.Marker([d_lat, d_lon], tooltip='click here for more', popup=destination,
#                       icon=folium.Icon(color='red', icon='cloud')).add_to(m)
#
#         # draw the line between location and destination
#         line = folium.PolyLine(locations=[pointA, pointB], weight=5, color='blue')
#         m.add_child(line)
#
#         instance.location = location
#         instance.distance = distance
#         instance.save()
#
#     # m = m._repr_html_()
#
#     context = {
#         'distance': distance,
#         'destination': destination,
#         'form': form,
#         'map': m,
#     }
#
#     # return render(request, 'measurements/main.html', context)
#     return HttpResponse('ip produced')
