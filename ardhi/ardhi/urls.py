"""ardhi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('regions/', include('regions.urls')),
    path('parcels/', include('parcels.urls')),
    # path('payments/', include('payments.urls')),
    # path('ownership/', include('ownership.urls')),
    # path('transaction/', include('transaction.urls')),

    # django rest framework urls
    # path('api/accounts/', include('accounts.api.urls', 'account_api'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

admin.site.site_header = "Ardhi Land Information System."
admin.site.site_title = "Ardhi LIS Admin Portal."
admin.site.index_title = "Welcome to Ardhi Land Information System."
