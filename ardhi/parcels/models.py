from django.contrib.gis.db import models
from django.template.defaultfilters import date
from django.conf import settings
import datetime
from django.core.serializers import serialize


# Create your models here.
class Uploads(models.Model):
    areah = models.FloatField('Area(Ha)', default=0)
    perm = models.FloatField('Perimeter', default=0)
    plotno = models.BigIntegerField('Plot NO', unique=True)
    lrnumber = models.CharField('LRNumber', max_length=80, unique=True)
    geom = models.PolygonField('Geometry', srid=4326)

    class Meta:
        db_table = 'uploads'
        verbose_name_plural = "uploads"

    def __str__(self):
        return self.lrnumber

    def allUploads(self):
        """ Returns all objects from the database as ageojson"""
        return self.objects.annotate(geometry=AsGeoJSON('geom'))

    def serialized(self):
        """returns all the uploads in a serialize format"""
        return serialize('geojson', self.objects.all())

    def getCentroid(self, id=None):
        """ Returns the centroid of a specified parcel"""
        if id:
            return self.objects.annotate(geometry=AsGeoJSON(Centroid('geom'))).get(id=id).geom
        return self.objects.annotate(geometry=AsGeoJSON(Centroid('geom')))

    def getNearestParcels(self, id):
        """ Returns the first 50 parcels with a specified parcel of land"""
        parcels = []
        parcel = self.objects.get(id=id).geom
        for parc in self.objects.annotate(distance=Distance('geom', parcel)):
            parcels.append(parc.distance)
        return sorted(parcels[:50])


class Parcels(models.Model):
    gid = models.IntegerField(primary_key=True)
    areah = models.FloatField('Area(Ha)', default=0)
    perm = models.FloatField('Perimeter', default=0)
    plotno = models.BigIntegerField('Plot NO', unique=True)
    lrnumber = models.CharField('LRNumber', max_length=80, unique=True)
    geom = models.PolygonField('Geometry', srid=4326)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Owner', blank=True,
                              null=True, default=None)

    class Meta:
        db_table = 'parcels'
        verbose_name_plural = "parcels"

    def __str__(self):
        return self.lrnumber

    def getCentroid(self, id):
        """ Returns the centroid of a specified parcel"""
        return self.objects.annotate(geometry=AsGeoJSON(Centroid('geom'))).get(id=id).geom

    def getNearestParcels(self, id):
        """ Returns the first 50 parcels with a specified parcel of land"""
        parcels = []
        parcel = self.objects.get(id=id).geom
        for parc in self.objects.annotate(distance=Distance('geom', parcel)):
            parcels.append(parc.distance)
        return sorted(parcels[:50])

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
        return "%s" % self.parcel.lrnumber

    class Meta:
        # Gives the proper plural name for admin
        db_table = 'parcel_details'
        verbose_name_plural = "parcel_details"
