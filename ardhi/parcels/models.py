from django.contrib.gis.db import models
from django.template.defaultfilters import date
from django.conf import settings
# from django.db import models
import datetime


# Create your models here.
class LandParcels(models.Model):
    id = models.BigIntegerField(primary_key=True)
    lrnumber = models.BigIntegerField()
    areah = models.FloatField()
    aream = models.FloatField()
    perm = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Owner', blank=True,
                              null=True, default=None)
    class Meta:
        db_table = 'naiparcels'
        verbose_name_plural = "naisparcels"

    def __str__(self):
        return self.lrnumber


class Parcels(models.Model):
    id = models.BigIntegerField(primary_key=True)
    lr_no = models.IntegerField('LR Number', unique=True)
    area_ha = models.FloatField('Area Ha', max_length=10)
    area_m = models.FloatField('Area M', max_length=10)
    perimeter = models.FloatField('Perimeter', max_length=10)
    geom = models.MultiPolygonField(srid=4326)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Owner', blank=True,
                              null=True, default=None)

    class Meta:
        db_table = 'parcels'
        verbose_name_plural = "parcels"

    def __str__(self):
        return self.lr_no

    # def save(self, *args, **kwargs):
    #     # if geom ends up as a Polygon, make it into a MultiPolygon
    #     if self.geom and isinstance(self.geom, geos.Polygon):
    #         self.geom = geos.MultiPolygon(self.geom)
    #
    #     super(Parcels).save(*args, **kwargs)

    @property
    def popup_content(self):
        popup = "<span>Parcel ID   :  </span>{}".format(self.id)
        popup += "<span>Owner      :  </span>{}".format(self.owner)
        popup += "<span>Perimeter  :  </span>{}".format(self.perimeter)
        popup += "<span>Area (m)   :  </span>{}".format(self.area_ha)
        popup += "<span>Plot Number:  </span>{}".format(self.lr_no)
        popup += "<span>Status   :  </span>{}".format(self.status)
        return popup


# model representing parcel details
class ParcelDetails(models.Model):
    AGRICULTURAL = 'A'
    RESIDENTIAL = 'R'
    COMMERCIAL = 'C'
    RECREATIONAL = 'RC'
    TRANSPORT = 'T'
    LAND_USE = [
        (AGRICULTURAL, 'Agricultural'),
        (RESIDENTIAL, 'Residential'),
        (COMMERCIAL, 'Commercial'),
        (RECREATIONAL, 'Recreational'),
        (TRANSPORT, 'Transport'),
    ]
    FREEHOLD = 'freehold'
    LEASEHOLD = 'leasehold'
    TENURE = [
        (FREEHOLD, 'Freehold'),
        (LEASEHOLD, 'Leasehold'),
    ]

    ON_SALE = 'on_sale'
    IN_USE = 'in_use'
    RESTRICTED = 'restricted'
    STATUS = [
        (ON_SALE, 'on sale'),
        (IN_USE, 'in use'),
        (RESTRICTED, 'restricted')
    ]

    parcel = models.OneToOneField(Parcels, blank=False, verbose_name='Parcels', null=False, on_delete=models.CASCADE,
                                  related_name="details", related_query_name="details")
    land_use = models.CharField('Land_use', max_length=15, choices=LAND_USE, default=None, blank=False, null=False)
    tenure = models.CharField('Tenure', max_length=10, choices=TENURE, default=None, blank=False, null=False)
    status = models.CharField('Status', max_length=10, choices=STATUS, default=IN_USE)
    improvements = models.CharField('Land Improvements', max_length=100, default='nil')
    encumbrances = models.CharField('Encumbrances', max_length=100, default='nil')
    purchase_date = models.DateTimeField('Purchase Date', )
    registered = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return "%s" % self.parcel.lr_no

    class Meta:
        # Gives the proper plural name for admin
        db_table = 'parcel_details'
        verbose_name_plural = "parcel_details"



