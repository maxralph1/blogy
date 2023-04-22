from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from . import views
from .forms import PasswordResetConfirmForm, CustomPasswordResetForm, UserLoginForm

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name="accounts/login.html",
        form_class=UserLoginForm),
        name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
    path('register/', views.register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>)/',
         views.account_activate, name='activate'),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset/password_reset_form.html',
            success_url='password_reset_email_confirm',
            email_template_name='accounts/password_reset/password_reset_email.html',
            form_class=CustomPasswordResetForm,
        ),
        name='password_reset',
    ),
    path(
        'password_reset_confirm/<uidb64>/<token>',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset/password_reset_confirm.html',
            success_url='password_reset_complete/',
            form_class=PasswordResetConfirmForm),
        name='password_reset_token_confirm'),
    path(
        'password_reset/password_reset_email_confirm/',
        TemplateView.as_view(
            template_name='accounts/password_reset/reset_status.html'),
        name='password_reset_emailed',
    ),
    path(
        'password_reset_confirm/Mg/password_reset_complete/',
        TemplateView.as_view(
            template_name='accounts/password_reset/reset_status.html'),
        name='password_reset_complete',
    ),


    # User dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile-photo/', views.profile_photo, name='profile_photo'),
    path('profile/delete_user/', views.delete_user, name='delete_user'),
    path(
        'profile/delete_confirm/',
        TemplateView.as_view(
            template_name='accounts/users/delete_confirm.html'),
        name='delete_confirmation',
    )
]
