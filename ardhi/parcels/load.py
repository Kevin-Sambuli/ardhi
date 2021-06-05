import os
from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import Parcels


# python manage.py ogrinspect world\data\TM_WORLD_BORDERS-0.3.shp Parcels --srid=4326 --mapping --multi

parcels_mapping = {
    'id': 'Id',
    'perimeter': 'perimeter',
    'area_ha': 'area_ha',
    'lr_no': 'Lr_No',
    'geom': 'MULTIPOLYGON',
}

# centroid_mapping = {
#     'id': 'Id',
#     'perimeter': 'perimeter',
#     'area_ha': 'area_ha',
#     'lr_no': 'Lr_No',
#     'geom': 'MULTIPOINT',
# }

parcels_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'shapefile', 'landparcels.shp'), )
# centroid_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'shapefile', 'centroid.shp'), )


def run(verbose=True):
    lm = LayerMapping(Parcels, parcels_shp, parcels_mapping, transform=False, encoding='utf-8')
    lm.save(strict=True, verbose=verbose)


# def run_centroids(verbose=True):
#     lm = LayerMapping(Centroids, centroid_shp, centroid_mapping, transform=False, encoding='utf-8')
#     lm.save(strict=True, verbose=verbose)
