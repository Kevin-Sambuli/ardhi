from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Account


class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'phone', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login',)
    list_display_links = ('email',)
    filter_horizontal = ()
    list_per_page = 10  # record 10 per page
    list_filter = ('is_staff', 'is_admin', 'is_superuser', 'is_active')
    fieldsets = ()


# Register your models here.
admin.site.register(Account, AccountAdmin)
