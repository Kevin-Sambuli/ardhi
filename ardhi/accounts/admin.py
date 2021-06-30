from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, Profile
from .forms import RegisterForm, AccountUpdateForm
from django.utils.translation import gettext_lazy as _


class AccountAdmin(UserAdmin):
    ordering = ["email"]
    add_form = AccountUpdateForm
    form = RegisterForm
    model = Account

    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login',)
    list_display_links = ('email',)
    filter_horizontal = ()
    list_per_page = 10
    list_filter = ('is_staff', 'is_admin', 'is_superuser', 'is_active')
    fieldsets = (
        (_("Login Credentials"), {"fields": ("email", "password",)},),

        (_("Personal Information"), {"fields": ("username", "first_name", "last_name")},),

        (_("Permissions and Groups"),
         {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions",)},),

        (_("Important Dates"), {"fields": ("last_login", "date_joined",)},),)

    add_fieldsets = (
    None, {"classes": ("wide",), "fields": ("email", "password1", "password2", "is_staff", "is_active",), },)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('owner', 'kra_pin', 'gender', 'id_no', 'dob', 'phone', 'profile_image')
    search_fields = ('owner',)
    readonly_fields = ('kra_pin', 'phone', 'id_no', 'dob', 'profile_image')
    list_display_links = ('owner',)
    filter_horizontal = ()
    list_per_page = 10


# Register your models here.
admin.site.register(Account, AccountAdmin)
admin.site.register(Profile, ProfileAdmin)
