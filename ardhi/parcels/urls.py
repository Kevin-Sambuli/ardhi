from django.urls import path
from django.views.generic import TemplateView
from djgeojson.views import GeoJSONLayerView
from .models import Parcels
from . import views

urlpatterns = [
    path('parcels/', GeoJSONLayerView.as_view(model=Parcels,
                                              properties=('id', 'owner', 'area_ha', 'perimeter', 'lr_no',)),
         name='data'),
    # path('map/', TemplateView.as_view(template_name='ownership/map.html'), name='map'),
    path('parcel_map/', TemplateView.as_view(template_name='parcels/parcels.html'), name='runda_parcels'),
    # path('my_parcels_map/', TemplateView.as_view(template_name='ownership/my_map.html'), name='my_map'),
    path('landparcels/', views.parcels, name='parcels'),
    # path('distance/', views.calculate_distance_view, name='distance'),
    path('centroids/', views.get_points, name='distance'),

]
