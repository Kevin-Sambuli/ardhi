from django.contrib.gis.db.models.functions import AsGeoJSON, Centroid, Distance
from .utils import get_geo, get_center_coordinates, get_zoom, get_ip_address
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core.serializers import serialize
from djgeojson.views import GeoJSONLayerView
from .models import Parcels, ParcelDetails
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from .database import get_cursor
from django import forms
from .map import my_map
import json, folium
from django.contrib.gis.geos import GEOSGeometry

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

# from .forms import MeasurementModelForm


def get_points(request):
    cur1 = get_cursor()  # first database connection instance
    cur2 = get_cursor()  # second database connection instance

    parcels_cent = Parcels.objects.annotate(geometry=AsGeoJSON(Centroid('geom')))
    data = []
    for parcel in parcels_cent:
        data.append(parcel)
    print(data)  # [ < Parcels: LR12872 / 26 >, < Parcels: LR12872 / 24 >, < Parcels: LR12872 / 23 >, ]

    for dat in data:
        print(dat.geometry)
        """ ill use zip function to combine the list of coordinates"""

    # ST_X(ST_Centroid(a.the_geom)) and ST_Y(ST_Centroid(a.the_geom))

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
    return HttpResponse(points_as_geojson, content_type='json')
    # return JsonResponse(json.loads(data))


def my_property(request):
    """ function that returns parcels of the logged in user  generate a folium leaflet map"""
    context = {}
    parcels_as_geojson = serialize('geojson', Parcels.objects.all())

    try:
        # returning my parcels as geojson to be passed on the map as objects
        my_parcel = serialize('geojson', Parcels.objects.filter(owner_id=request.user.id))

        # accessing parcels of the logged user
        my_own_parcels = Parcels.objects.filter(owner_id=request.user.id)

        #  getting each parcel details
        details = [ParcelDetails.objects.get(parcel=parcel_id) for parcel_id in my_own_parcels]

        # accessing each parcel detail and returning each parcel id
        # data = [det for det in Parcels.objects.filter(owner_id=request.user.id).values_list('id', flat=True)]

        # Generating folium leaflet map using my_map function
        m = my_map(land_parcels=parcels_as_geojson, parcel=my_parcel)
        m = m._repr_html_()

        context['map'] = m
        context['details'] = details
        context['parcels'] = my_own_parcels
    except:
        print('You dont own parcels in the system')
        m = my_map(land_parcels=parcels_as_geojson)
        m = m._repr_html_()
        context['map'] = m

    return render(request, 'parcels/map.html', context)


def parcel_render_pdf(request, *args, **kwargs):
    context = {}
    parcels_as_geojson = serialize('geojson', Parcels.objects.all())

    my_parcel = serialize('geojson', Parcels.objects.filter(owner_id=request.user.id))

    my_own_parcels = Parcels.objects.filter(owner_id=request.user.id)

    details = [ParcelDetails.objects.get(parcel=parcel_id) for parcel_id in my_own_parcels]

    m = my_map(land_parcels=parcels_as_geojson, parcel=my_parcel)
    m = m._repr_html_()

    context['map'] = m
    context['details'] = details
    context['parcels'] = my_own_parcels

    template_path = 'parcels/pdf.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename ="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



def render_pdf_view(request):
    template_path = 'pdf.html'
    context = {'myvar': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"' """in the"""
    response['Content-Disposition'] = 'filename ="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def search_parcels(request):
    """ function that returns parcels in geojson and generate a folium leaflet map

    returning the centroid of the searched parcel calculate the distance to that point

    should also return the parcel details of that parcel and produce the pdf of the parcel, map, and parcel details"""
    context = {}
    points_as_geojson = serialize('geojson', Parcels.objects.all())

    qu = get_cursor()
    ids = 84

    # parcels search and returning the centroid then placed on the map
    try:

        parcel = serialize('geojson', Parcels.objects.filter(owner_id=request.user.id))

        # accessing each parcel detail and returning each parcel id
        parcel_id = list(Parcels.objects.filter(owner_id=request.user.id).values_list('id', flat=True))
        details = [det for det in list(Parcels.objects.filter(owner_id=request.user.id).values_list('id', flat=True))]

        # qu.execute('select ST_AsText(ST_Centroid(geom) ) FROM parcels;')# where id=84;')
        qu.execute(f'select ST_AsText(ST_Centroid(geom) ) FROM parcels where id={ids};')
        mmap = qu.fetchall()
        # if mmap:
        print('map =', mmap)
        print('point', str(mmap[0][0]))

        pnt = GEOSGeometry(str(mmap[0][0]), srid=4326)
        print('geos point object', pnt)

        print('tuple of coordinates =', pnt.coords)
        print('list of coordinates =', list(pnt.coords))

        pins = list(pnt.coords)
        pin1, pin2 = float(pins[0]), float(pins[1])
        print('lng =', pin1, 'lat =', pin2)

        # Generating folium leaflet map using my_map function
        m = my_map(land_parcels=points_as_geojson, parcel=parcel, lng=pnt.coords[0], lat=pnt.coords[1])
        m = m._repr_html_()
        context['map'] = m
    except:
        print('the parcel does not exist')

        # qu = get_cursor()
        # qu.execute("""SELECT jsonb_build_object('type','FeatureCollection','features', jsonb_agg(features.feature))
        #     FROM ( SELECT jsonb_build_object( 'type','Feature','geometry', ST_AsGeoJSON(geom)::jsonb,'properties',
        #     to_jsonb(inputs)  -'geom') AS feature, 'geometry'
        #     FROM (SELECT * FROM njiruproj) inputs) features;""")
        # data = qu.fetchall()
        # m = my_map(land_parcels=data[0][0])

        m = my_map(land_parcels=points_as_geojson)
        m = m._repr_html_()
        context['map'] = m

    return render(request, 'parcels/map.html', context)


def parcels_within_3km(request):
    """Get parcels that are at least 3km or less from a users location"""
    pol = serialize('geojson', Parcels.objects.annotate(geometry=AsGeoJSON(Centroid('geom'))))
    # # parcel = Parcels.objects.annotate(geometry=Centroid('geom'))
    #
    parcels = Parcels.objects.annotate(geometry=AsGeoJSON(Centroid('geom'))).get(id=84).geom
    data1 = []
    for parc in Parcels.objects.annotate(geometry=AsGeoJSON(Centroid('geom')), distance=Distance('geom', parcels)):
        print(parc.lr_no, parc.distance)
        data1.append(parc.distance)

    ip = get_ip_address(request)

    print('distance 1', sorted(data1))
    print('ip address', ip)

    # parcels = Parcels.objects.annotate(geometry=AsGeoJSON(Centroid('geom'))).get(id=84).geom
    parcels = Parcels.objects.get(id=84).geom
    data2 = []
    for parc in Parcels.objects.annotate(distance=Distance('geom', parcels)):
        # print(parc.lr_no, parc.distance)
        data2.append(parc.distance)

    sorted(data2)
    # print('distance 2', data2[:10])

    return HttpResponse(pol, content_type='json')


def calculate_distance_view(request):
    # initial values
    distance = None
    destination = None

    # obj = get_object_or_404(Measurement, id=1)
    # form = MeasurementModelForm(request.POST or None)

    geolocator = Nominatim(user_agent='parcels')

    ip = '192.168.0.1'
    country, city, lat, lon = get_geo(ip)
    print('country', country)
    print('city', city)
    print('lat', lat)
    print('lng', lon)
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

    # if form.is_valid():
    #     instance = form.save(commit=False)
    #     destination_ = form.cleaned_data.get('destination')
    #     destination = geolocator.geocode(destination_)
    #
    #     # destination coordinates
    #     d_lat = destination.latitude
    #     d_lon = destination.longitude
    #     pointB = (d_lat, d_lon)
    #     # distance calculation
    #     distance = round(geodesic(pointA, pointB).km, 2)
    #
    #     # folium map modification
    #     m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon, d_lat, d_lon),
    #                    zoom_start=get_zoom(distance))
    #     # location marker
    #     folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=city['city'],
    #                   icon=folium.Icon(color='purple')).add_to(m)
    #     # destination marker
    #     folium.Marker([d_lat, d_lon], tooltip='click here for more', popup=destination,
    #                   icon=folium.Icon(color='red', icon='cloud')).add_to(m)
    #
    #     # draw the line between location and destination
    #     line = folium.PolyLine(locations=[pointA, pointB], weight=5, color='blue')
    #     m.add_child(line)
    #
    #     instance.location = location
    #     instance.distance = distance
    #     instance.save()
    #
    # m = m._repr_html_()
    #
    # context = {
    #     'distance': distance,
    #     'destination': destination,
    #     'form': form,
    #     'map': m,
    # }

    return HttpResponse('printed')
    # return render(request, 'measurements/main.html', context)

    # longitude = request.GET.get("lon", None)
    # latitude = request.GET.get("lat", None)

    # if longitude and latitude:
    #     user_location = Point(float(longitude), float(latitude), srid=4326)
    #     closest_parcels = Parcels.objects.filter(geom__distance_lte=(user_location, D(km=3)))
    #     parcels= serialize('geojson', Parcels.objects.filter(geom__distance_lte=(user_location, D(km=3))))

    #     return HttpResponse(parcels, content_type='json')

    #     serializer = self.get_serializer_class()
    #     serialized_hospitals = serializer(closest_hospitals, many=True)
    #     return Response(serialized_hospitals.data, status=status.HTTP_200_OK)
    # return Response(status=status.HTTP_400_BAD_REQUEST)

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
