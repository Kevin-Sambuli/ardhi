from django.apps import AppConfig

from ardhi.accounts import geolocation


class GeolocationConfig(AppConfig):
    name = geolocation
