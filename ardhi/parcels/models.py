from django.template.defaultfilters import date
from django.contrib.gis.db import models
from django.conf import settings
import datetime


# Create your models here.
class Parcels(models.Model):
    ON_SALE = 'on_sale'
    IN_USE = 'in_use'
    STATUS = [
        (ON_SALE, 'on sale'),
        (IN_USE, 'in use')
    ]
    id = models.BigIntegerField(primary_key=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Owner', blank=True,
                              null=True, default=None)
    perimeter = models.FloatField('Perimeter', max_length=10)
    area_ha = models.FloatField('Area', max_length=10)
    lr_no = models.CharField('LR Number', max_length=10)
    status = models.CharField('Status', max_length=10, choices=STATUS, default=IN_USE)
    geom = models.MultiPolygonField(srid=4326)

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

    parcel = models.OneToOneField(Parcels, blank=False, verbose_name='Parcels', null=False, on_delete=models.CASCADE,
                                  related_name="details", related_query_name="details")
    land_use = models.CharField('Land_use', max_length=15, choices=LAND_USE, default=None, blank=False, null=False)
    tenure = models.CharField('Tenure', max_length=10, choices=TENURE, default=None, blank=False, null=False)
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

# class Centroids(models.Model):
#     id = models.BigIntegerField(primary_key=True)
#     owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Owner', blank=True,
#                               null=True, default=None)
#     perimeter = models.FloatField()
#     area_ha = models.FloatField()
#     lr_no = models.CharField(max_length=10)
#     geom = models.MultiPointField(srid=4326)

#     class Meta:
#         db_table = 'centroids'
#         verbose_name_plural = "centroid"

#     def __str__(self):
#         return self.lr_no
