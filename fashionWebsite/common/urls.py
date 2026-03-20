from django.urls import path, include

from fashionWebsite.common import views

urlpatterns = [
    path('', views.BaseView.as_view(), name='base'),
]