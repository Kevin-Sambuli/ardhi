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
    path('try/', views.parcels2, name='jparcels'),
    path('property/', views.my_property, name='map'),
    path('pdf/', views.parcel_render_pdf, name='pdf'),
    path('search/', views.search_parcels, name='search'),
    path('distance/', views.parcels_within_3km, name='distance'),
    # path('distance/', views.my_parcels, name='distance'),
    path('distance2/', views.calculate_distance_view, name='distance2'),
    path('rundamap/', TemplateView.as_view(template_name='parcels/parcels.html'), name='rundamap'),
    path('maps/', TemplateView.as_view(template_name='parcels/parcel2.html'), name='parcels'),
]
