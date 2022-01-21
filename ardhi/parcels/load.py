import os
from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import Parcels ,LandParcels

# python manage.py ogrinspect parcels\shapefile\landparcels.shp ParcelLand --srid=4326 --mapping --multi
# python manage.py shell

# Auto-generated `LayerMapping` dictionary for Parcels model
parcels_mapping = {
    'id': 'Id',
    'lr_no': 'LRNumber',
    'area_ha': 'AreaH',
    'area_m': 'AreaM',
    'perimeter': 'PerM',
    'geom': 'MULTIPOLYGON',
}


land_parcels_mapping = {
    'areah': 'AreaH',
    'perm': 'PerM',
    'aream': 'AreaM',
    'lrnumber': 'LRNumber',
    'id': 'Id',
    'geom': 'MULTIPOLYGON',
}


parcels_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'shapefile', 'nairobi.shp'), )


# centroids_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'shapefile', 'landparcels.shp'), )
land_parcels_mapping_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'shapefile', 'nairobi.shp'), )


def run(verbose=True):
    lm = LayerMapping(Parcels, parcels_shp, parcels_mapping, transform=False, encoding='utf-8')
    lm.save(strict=True, verbose=verbose)


def run_parcels(verbose=True):
    lm = LayerMapping(LandParcels, land_parcels_mapping_shp, land_parcels_mapping, transform=False, encoding='utf-8')
    lm.save(strict=True, verbose=verbose)
