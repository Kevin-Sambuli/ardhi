# from django.views.generic import TemplateView
# from django.conf.urls.static import static
from django.urls import path, include
# from django.conf import settings
from . import views

urlpatterns = [
    path('search/', views.search_view, name='search'),
]
