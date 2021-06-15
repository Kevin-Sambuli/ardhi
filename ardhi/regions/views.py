import json
from django.http import JsonResponse, HttpResponse
from django.core.serializers import serialize
from djgeojson.views import GeoJSONLayerView

from .models import Counties, SubLocations, Locations, SubCounties
from .map import my_map


def region_map(request):
    counties = serialize('geojson', Counties.objects.filter(coucode=47))
    map2 = my_map(counties=counties, )  # subcounties=subcounty, locations=locations, sublocations=subloc)
    map2.save('regions/templates/regions/map.html')

    return HttpResponse(counties, content_type='json')
