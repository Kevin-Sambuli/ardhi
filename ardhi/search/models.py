from django.conf import settings
from django.db import models
import reportlab


# Create your models here.
class PropertySearch(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Owner', blank=False,
                              null=False, default=None)
    parcel = models.CharField('Parcel', max_length=10, blank=False, null=False)
    purpose = models.TextField('Purpose', max_length=200, blank=False, null=False, )
    date = models.DateTimeField('Date', auto_now_add=True)

    class Meta:
        db_table = 'landsearch'
        verbose_name = "Land Search"
        verbose_name_plural = "Land Search"

    def __str__(self):
        return self.owner

