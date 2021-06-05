import os
from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import Counties, SubCounties, Locations, SubLocations


# python manage.py ogrinspect world\data\TM_WORLD_BORDERS-0.3.shp Parcels --srid=4326 --mapping --multi

county_mapping = {
    'coucode': 'CouCode',
    'first_coun': 'FIRST_CouN',
    'geom': 'MULTIPOLYGON'
}

subcounties_mapping = {
    'sccodefull': 'SCCodeFull',
    'first_scou': 'FIRST_SCou',
    'geom': 'MULTIPOLYGON',
}

locations_mapping = {
    'loccodeful': 'LocCodeFul',
    'first_locn': 'FIRST_LocN',
    'geom': 'MULTIPOLYGON',
}

sublocations_mapping = {
    'slcodefull': 'SlCodeFull',
    'first_slna': 'FIRST_SLNa',
    'geom': 'MULTIPOLYGON',
}

counties_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'shapefile', '2019_Countiies.shp'), )
subcounty_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'shapefile', '2019_SubCountiies.shp'), )
location_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'shapefile', '2019_Locations.shp'), )
subloc_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'shapefile', '2019_SubLocations.shp'), )


def county_run(verbose=True):
    lm = LayerMapping(Counties, counties_shp, county_mapping, transform=False, encoding='utf-8')
    lm.save(strict=True, verbose=verbose)

def subcounty_run(verbose=True):
    lm = LayerMapping(SubCounties, subcounty_shp, subcounties_mapping, transform=False, encoding='utf-8')
    lm.save(strict=True, verbose=verbose)

def location_run(verbose=True):
    lm = LayerMapping(Locations, location_shp, locations_mapping, transform=False, encoding='utf-8')
    lm.save(strict=True, verbose=verbose)

def subloc_run(verbose=True):
    lm = LayerMapping(SubLocations, subloc_shp, sublocations_mapping, transform=False, encoding='utf-8')
    lm.save(strict=True, verbose=verbose)
