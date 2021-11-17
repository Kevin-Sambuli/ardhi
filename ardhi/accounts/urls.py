from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.registration_view, name='register'),
    path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),
    path('profile/', views.profile_view, name='profile'),
    path('edit_account/', views.edit_account, name='edit_account'),
    path('update_password/', views.update_password, name='update_password'),
    # path('my_parcels_map/', TemplateView.as_view(template_name='accounts/realtime_location.html'), name='location'),
    path('success/', TemplateView.as_view(template_name='accounts/success.html'), name='success'),

    # path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html'),
    #      name='password_reset'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
         name='password_change_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
]
