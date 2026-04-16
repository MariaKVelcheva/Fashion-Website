from django.urls import path
from django.contrib.auth import views as auth_views

from fashionWebsite.accounts import views

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    path('update/', views.UpdateCustomerView.as_view(), name='customer-update'),
    path('details/', views.DetailsCustomerView.as_view(), name='customer-details'),
    path('delete/', views.DeleteUserView.as_view(), name='user-delete'),
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
             email_template_name='accounts/password-management/password_reset_email.html',
             subject_template_name='accounts/password-management/password_reset_subject.txt'
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
