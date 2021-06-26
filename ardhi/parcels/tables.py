import django_tables2 as tables
from .models import Parcels, ParcelDetails


class PersonTable(tables.Table):
    class Meta:
        model = Parcels
        template_name = "django_tables2/bootstrap.html"
        fields = ("name",)
