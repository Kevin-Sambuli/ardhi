from django.conf import settings
from django.db import models
import reportlab


# Create your models here.
class PropertyTransfer(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Owner', blank=False,
                              null=False, default=None)
    buyer_email = models.EmailField(verbose_name="Buyer's email", blank=False, null=False, max_length=100)
    parcel_no = models.IntegerField(blank=False, null=False, verbose_name="Parcel No")
    amount = models.IntegerField(blank=False, null=False, verbose_name="Amount")
    file_upload = models.FileField(upload_to='documents/')
    transfer_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'transfers'
        verbose_name_plural = "transfers"

    def __str__(self):
        return self.buyer_email


# class Subdivision(models.Model):
#     email = models.EmailField(verbose_name="Email", blank=False, null=False, max_length=100, default=None)
#     parcel_no = models.CharField(max_length=10, blank=False, null=False)
#     reason = models.TextField(max_length=200, blank=False, null=False)
#     subdivision_date = models.DateTimeField()
#
#     class Meta:
#         db_table = 'subdivisions'
#         verbose_name_plural = "subdivisions"
#
#     def __str__(self):
#         return self.email
#     class Meta:
#         db_table = 'land_transfer'
#         verbose_name = "Land Transfer"
#         verbose_name_plural = "Land Transfer"
#
#     def __str__(self):
#         return self.parcel
