from django.urls import path
from django.views.generic import TemplateView
from djgeojson.views import GeoJSONLayerView
from .models import Parcels
from . import views

urlpatterns = [
    path('data/', GeoJSONLayerView.as_view(model=Parcels,
                                           properties=('id', 'owner', 'area_ha', 'perimeter', 'lr_no','status')), name='data'),
    path('centroids/', views.get_points, name='distance'),
    path('json/', views.parcels, name='json_parcels'),
    path('map/', views.my_parcels, name='map'),
    # path('distance/', views.parcels_within_3km, name='json_parcels'),
    path('rundamap/', TemplateView.as_view(template_name='parcels/parcels.html'), name='rundamap'),
    # path('map/', TemplateView.as_view(template_name='parcels/parcel2.html'), name='parcels'),



]
