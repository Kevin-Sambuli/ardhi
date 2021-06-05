import json

from django import forms
from django.http import JsonResponse, HttpResponse
from django.core.serializers import serialize
from djgeojson.views import GeoJSONLayerView

from .models import Counties, SubLocations, Locations, SubCounties
from .map import my_map
# from .database import get_cursor

# from django.shortcuts import render, get_object_or_404
# from .utils import get_geo, get_center_coordinates, get_zoom
# from geopy.geocoders import Nominatim
# from geopy.distance import geodesic
# import folium


# # from .forms import MeasurementModelForm


def region_map(request):
    print('counties', list(Counties.objects.all().value_list('first_coun', flat=True)))
    # print('subcounty', SubCounties.objects.all())
    # print('Locations', Locations.objects.all())
    # print('sublocations', SubLocations.objects.all())

    counties = serialize('geojson', Counties.objects.filter(coucode=47))
    # subcounty = serialize('geojson', SubCounties.objects.all())
    # locations = serialize('geojson', Locations.objects.all())
    # subloc = serialize('geojson', SubLocations.objects.all())
    # map2 = my_map(counties=counties, subcounties=subcounty, locations=locations, sublocations=subloc)
    # map2.save('regions/templates/regions/map.html')

    return HttpResponse(counties, content_type='json')
    # return JsonResponse(json.loads(counties))


# # class ParcelGeoJson(GeoJSONLayerView):
# #     model = Parcels
# #     properties = ('popup_content',)
# #
# #
# # def parcel_js(request):
# #     parcel = Parcels.objects.all()
# #     context = {'object_list': parcel,}
# #     return render(request, 'poco/poco_js.html', context)


# def get_points(request):
#     cur = get_cursor()
#     # cur.execute("""SELECT json_build_object('type', 'Feature','geometry', ST_AsGeoJSON(the_geom :: geometry) :: json,
#     # 'properties', json_build_object('name', name)) jsonb FROM parcels;""")

#     # queryset_parcels = ("""SELECT jsonb_build_object('type','FeatureCollection','features', jsonb_agg(features.feature))
#     #        FROM ( SELECT jsonb_build_object( 'type','Feature','geometry', ST_AsGeoJSON(geom)::jsonb,'properties',
#     #        to_jsonb(inputs)  -'geom') AS feature, 'geometry'
#     #        FROM (SELECT * FROM parcels) inputs) features;""")

#     query1 = ('SELECT jsonb_build_object FROM public.parcels_json;')
#     cur.execute(query1)

#     # query_set_centroids = ("""SELECT jsonb_build_object('type','FeatureCollection','features', jsonb_agg(
#     # features.feature)) FROM ( SELECT jsonb_build_object( 'type','Feature','geometry', ST_AsGeoJSON(ST_Centroid(
#     # geom))::jsonb,'properties',  to_jsonb(inputs)  -'geom') AS feature, 'geometry' FROM (SELECT * FROM parcels)
#     # inputs) features;""")

#     query2 = ('SELECT jsonb_build_object FROM public.centroids_json;')
#     cur.execute(query2)

#     parcel = cur.fetchall()
#     centroids_json = parcel[0][0]
#     print('parcel', parcel)
#     print('centroids', centroids_json)
#     return JsonResponse(centroids_json)

# # def calculate_distance_view(request):
# #     # initial values
# #     distance = None
# #     destination = None
# #
# #     obj = get_object_or_404(Parcels, id=1)
# #     form = MeasurementModelForm(request.POST or None)
# #     geolocator = Nominatim(user_agent='measurements')
# #
# #     ip = '72.14.207.99'
# #     country, city, lat, lon = get_geo(ip)
# #     location = geolocator.geocode(city)
# #
# #     # location coordinates
# #     l_lat = lat
# #     l_lon = lon
# #     pointA = (l_lat, l_lon)
# #
# #     # initial folium map
# #     m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon), zoom_start=8)
# #     # location marker
# #     folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=city['city'],
# #                   icon=folium.Icon(color='purple')).add_to(m)
# #
# #     if form.is_valid():
# #         instance = form.save(commit=False)
# #         destination_ = form.cleaned_data.get('destination')
# #         destination = geolocator.geocode(destination_)
# #
# #         # destination coordinates
# #         d_lat = destination.latitude
# #         d_lon = destination.longitude
# #         pointB = (d_lat, d_lon)
# #         # distance calculation
# #         distance = round(geodesic(pointA, pointB).km, 2)
# #
# #         # folium map modification
# #         m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon, d_lat, d_lon),
# #                        zoom_start=get_zoom(distance))
# #         # location marker
# #         folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=city['city'],
# #                       icon=folium.Icon(color='purple')).add_to(m)
# #         # destination marker
# #         folium.Marker([d_lat, d_lon], tooltip='click here for more', popup=destination,
# #                       icon=folium.Icon(color='red', icon='cloud')).add_to(m)
# #
# #         # draw the line between location and destination
# #         line = folium.PolyLine(locations=[pointA, pointB], weight=5, color='blue')
# #         m.add_child(line)
# #
# #         instance.location = location
# #         instance.distance = distance
# #         instance.save()
# #
# #     # m = m._repr_html_()
# #
# #     context = {
# #         'distance': distance,
# #         'destination': destination,
# #         'form': form,
# #         'map': m,
# #     }
# #
# #     # return render(request, 'measurements/main.html', context)
# #     return HttpResponse('ip produced')
