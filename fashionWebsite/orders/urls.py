from django.urls import path, include

from fashionWebsite.orders import views

urlpatterns = [
    path("promotions/", include([
        path("", views.PromotionsCatalogueView.as_view(), name="all-promotions"),
        path("create/", views.CreatePromotionView.as_view(), name="create-promotion"),
        path("update/<int:pk>/", views.UpdatePromotionView.as_view(), name="update-promotion"),
    ]))
]

