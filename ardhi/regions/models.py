# from django.db import models
from django.contrib.gis.db import models
import datetime
from django.conf import settings
from django.template.defaultfilters import date


# Create your models here.
class Counties(models.Model):
    coucode = models.CharField(max_length=2, unique=True)
    first_coun = models.CharField(max_length=30, unique=True)
    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        db_table = 'counties'
        verbose_name_plural = "counties"

    def __str__(self):
        return self.first_coun

    @property
    def popup_content(self):
        popup = "<span>County Code   :  </span>{}".format(self.coucode)
        popup += "<span>County Name  :  </span>{}".format(self.first_coun)
        return popup


class SubCounties(models.Model):
    sccodefull = models.CharField(max_length=4)
    first_scou = models.CharField(max_length=30)
    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        db_table = 'subcounties'
        verbose_name_plural = "subcounties"

    def __str__(self):
        return self.first_scou

    @property
    def popup_content(self):
        popup = "<span>SubCounty Code   :  </span>{}".format(self.sccodefull)
        popup += "<span>SubCounty Name  :  </span>{}".format(self.first_scou)
        return popup


class Locations(models.Model):
    loccodeful = models.CharField(max_length=8)
    first_locn = models.CharField(max_length=30)
    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        db_table = 'locations'
        verbose_name_plural = "locations"

    def __str__(self):
        return self.first_locn

    @property
    def popup_content(self):
        popup = "<span>Location Code   :  </span>{}".format(self.loccodeful)
        popup += "<span>Location Name  :  </span>{}".format(self.first_locn)
        return popup


class SubLocations(models.Model):
    slcodefull = models.CharField(max_length=10)
    first_slna = models.CharField(max_length=30)
    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        db_table = 'sublocations'
        verbose_name_plural = "sublocations"

    def __str__(self):
        return self.first_slna

    @property
    def popup_content(self):
        popup = "<span>Subloc Code   :  </span>{}".format(self.slcodefull)
        popup += "<span>Subloc Name  :  </span>{}".format(self.first_slna)
        return popup
