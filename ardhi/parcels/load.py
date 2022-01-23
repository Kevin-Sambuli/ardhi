import os
# from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import Parcels, Uploads

# python manage.py ogrinspect parcels\shapefile\landparcels.shp ParcelLand --srid=4326 --mapping --multi
# python manage.py shell

# Auto-generated `LayerMapping` dictionary for Parcels model
parcels_mapping = {
    'areah': 'AreaH',
    'perm': 'PerM',
    'aream': 'AreaM',
    'plotno': 'PlotNo',
    'lrnumber': 'LRNumber',
    'geom': 'MULTIPOLYGON',
}

# parcels_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'shapefile', 'nairobi.shp'), )
parcels_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'shapefile', 'plots.shp'), )


def run(verbose=True):
    lm = LayerMapping(Uploads, parcels_shp, parcels_mapping, transform=False, encoding='utf-8')
    lm.save(strict=True, verbose=verbose)
    # fid_range=(0, 10))

