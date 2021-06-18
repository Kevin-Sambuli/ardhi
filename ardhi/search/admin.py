from django.contrib import admin
from .models import PropertySearch


# Register your models here.
class ParcelSearchAdmin(admin.ModelAdmin):
    list_display = ('owner', 'parcel', 'date')
    list_display_links = ('owner',)
    list_per_page = 10
    readonly_fields = ('owner','parcel',)
    search_fields = ('owner',)
    filter_horizontal = ()
    list_filter = ('parcel',)
    fieldsets = ()


admin.site.register(PropertySearch, ParcelSearchAdmin)