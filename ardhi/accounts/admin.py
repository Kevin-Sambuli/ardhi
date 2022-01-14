from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, Profile, Landowner, Manager, Agent
from .forms import RegisterForm, AccountUpdateForm
from django.utils.translation import gettext_lazy as _


admin.site.register(Landowner)
admin.site.register(Agent)
admin.site.register(Manager)


class AccountAdmin(UserAdmin):
    ordering = ["email"]
    add_form = AccountUpdateForm
    form = RegisterForm
    model = Account

    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_active', 'is_admin', 'is_staff','type')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login',)
    list_display_links = ('email',)
    filter_horizontal = ()
    list_per_page = 10
    list_filter = ('is_staff', 'type','is_admin', 'is_superuser', 'is_active')
    fieldsets = (
        (_("Login Credentials"), {"fields": ("email", "password",)},),

        (_("Personal Information"), {"fields": ("username", "first_name", "last_name")},),

        (_("Permissions and Groups"),
         {"fields": ("type","is_active", "is_staff", "is_superuser", "groups", "user_permissions",)},),

        (_("Important Dates"), {"fields": ("last_login", "date_joined",)},),)

    add_fieldsets = (
    None, {"classes": ("wide",), "fields": ("email", "password1", "password2", "is_staff", "is_active",), },)

    def active(self, obj):
        return obj.is_active == 1

    active.boolean = True

    def make_active(modeladmin, request, queryset):
        queryset.update(is_active=1)
        messages.success(request, "Selected Record(s) Marked as Active Successfully !!")

    def make_inactive(modeladmin, request, queryset):
        queryset.update(is_active=0)
        messages.success(request, "Selected Record(s) Marked as Inactive Successfully !!")

    admin.site.add_action(make_active, "Make Active")
    admin.site.add_action(make_inactive, "Make Inactive")


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
