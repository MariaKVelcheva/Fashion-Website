from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include("fashionWebsite.common.urls")),
    path('admin/', admin.site.urls),
    path('accounts/', include("fashionWebsite.accounts.urls")),
    path('clothes/', include("fashionWebsite.clothes.urls")),
]


password_patterns = [
    path('password-change/',
         auth_views.PasswordChangeView.as_view(
             template_name="accounts/password-management/password-change.html"),
         name="password-change"),
    path('password-change/done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name="accounts/password-management/password-change-done.html"),
         name="password-change-done"),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password-management/password-reset.html',
             email_template_name='accounts/password_reset_email.html',
             subject_template_name='accounts/password_reset_subject.txt'
         ),
         name="password-reset"),
    path('password-reset/confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="accounts/password-management/password-reset-confirm.html"),
         name="password-reset-confirm"),
    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="accounts/password-management/password-reset-complete.html"),
         name="password_reset_complete"),
]


urlpatterns += password_patterns

