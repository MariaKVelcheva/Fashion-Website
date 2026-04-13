from django.urls import path, include

from fashionWebsite.common import views

urlpatterns = [
    path('', views.BaseView.as_view(), name='home'),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("faq/", views.FAQView.as_view(), name="faq"),
    path("sales-conditions/", views.SalesConditionsView.as_view(), name="sales-conditions"),
]