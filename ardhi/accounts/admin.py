from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, GeoLocation, Address, Profile


class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login',)
    list_display_links = ('email',)
    filter_horizontal = ()
    list_per_page = 10
    list_filter = ('is_staff', 'is_admin', 'is_superuser', 'is_active')
    fieldsets = ()


class AddressAdmin(admin.ModelAdmin):
    list_display = ('owner', 'street', 'city', 'code',)
    search_fields = ('owner',)
    readonly_fields = ('street', 'city', 'code',)
    list_display_links = ('owner',)
    filter_horizontal = ()
    list_per_page = 10


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('owner', 'kra_pin', 'gender', 'id_no', 'dob', 'phone', 'profile_image')
    search_fields = ('owner',)
    readonly_fields = ('kra_pin', 'phone', 'id_no', 'dob', 'profile_image')
    list_display_links = ('owner',)
    filter_horizontal = ()
    list_per_page = 10


class GeoLocationAdmin(admin.ModelAdmin):
    list_display = ('owner', 'city', 'latitude', 'longitude')
    search_fields = ('country_name', 'city')
    readonly_fields = ('country_name', 'city', 'latitude', 'longitude')
    list_display_links = ('owner',)
    filter_horizontal = ()
    list_per_page = 10


# Register your models here.
admin.site.register(Account, AccountAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(GeoLocation, GeoLocationAdmin)
