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


# from .forms import MeasurementModelForm


def get_points(request):
    cur1 = get_cursor()  # first database connection instance
    cur2 = get_cursor()  # second database connection instance

    # return parcel data in geojson format
    query1 = ('SELECT jsonb_build_object FROM public.parcels_json;')
    cur1.execute(query1)

    # return the centroids of all parcels
    query2 = ('SELECT jsonb_build_object FROM public.centroids_json;')
    cur2.execute(query2)

    centroids = cur2.fetchall()
    centroids_json = centroids[0][0]
    return JsonResponse(centroids_json)


def parcels(request):
    """ function that returns parcels in geojson and generate a folium leaflet map"""
    points_as_geojson = serialize('geojson', Parcels.objects.all())
    parcel = serialize('geojson', Parcels.objects.filter(owner_id=request.user.id))

    # Generating folium leaflet map using my_map function
    map2 = my_map(parcel=parcel, land_parcels=points_as_geojson)
    map2.save('parcels/templates/parcels/ownership_map.html')

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


def calculate_distance_view(request):
    # initial values
    distance = None
    destination = None

    obj = get_object_or_404(Parcels, id=1)
    form = MeasurementModelForm(request.POST or None)
    geolocator = Nominatim(user_agent='measurements')

    ip = '72.14.207.99'
    country, city, lat, lon = get_geo(ip)
    location = geolocator.geocode(city)

    # location coordinates
    l_lat = lat
    l_lon = lon
    pointA = (l_lat, l_lon)

    # initial folium map
    m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon), zoom_start=8)
    # location marker
    folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=city['city'],
                  icon=folium.Icon(color='purple')).add_to(m)

    if form.is_valid():
        instance = form.save(commit=False)
        destination_ = form.cleaned_data.get('destination')
        destination = geolocator.geocode(destination_)

        # destination coordinates
        d_lat = destination.latitude
        d_lon = destination.longitude
        pointB = (d_lat, d_lon)
        # distance calculation
        distance = round(geodesic(pointA, pointB).km, 2)

        # folium map modification
        m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon, d_lat, d_lon),
                       zoom_start=get_zoom(distance))
        # location marker
        folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=city['city'],
                      icon=folium.Icon(color='purple')).add_to(m)
        # destination marker
        folium.Marker([d_lat, d_lon], tooltip='click here for more', popup=destination,
                      icon=folium.Icon(color='red', icon='cloud')).add_to(m)

        # draw the line between location and destination
        line = folium.PolyLine(locations=[pointA, pointB], weight=5, color='blue')
        m.add_child(line)

        instance.location = location
        instance.distance = distance
        instance.save()

    # m = m._repr_html_()

    context = {
        'distance': distance,
        'destination': destination,
        'form': form,
        'map': m,
    }

    # return render(request, 'measurements/main.html', context)
    return HttpResponse('ip produced')
