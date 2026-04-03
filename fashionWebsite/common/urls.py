from django.urls import path, include

from fashionWebsite.common import views

urlpatterns = [
    path('', views.BaseView.as_view(), name='home'),
    path("contact/", views.ContactView.as_view(), name="contact"),
]