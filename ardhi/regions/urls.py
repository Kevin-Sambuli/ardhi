from django.contrib import admin
from django.urls import path, include
# from .views import
from django.views.generic import TemplateView

from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('map_json/', views.region_map, name='map_json'),
    path('map_leaf/', TemplateView.as_view(template_name='regions/map.html'), name='map'),
]
