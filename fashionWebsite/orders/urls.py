from django.urls import path, include

from fashionWebsite.orders import views

urlpatterns = [
    path("promotions/", include([
        path("", views.PromotionsCatalogueView.as_view(), name="all-promotions"),
        path("create/", views.CreatePromotionView.as_view(), name="create-promotion"),
        path("update/<int:pk>/", views.UpdatePromotionView.as_view(), name="update-promotion"),
    ])),
    path("cart/add/<int:garment_id>/", views.add_to_cart, name="add-to-cart"), #or prduct?
    path("cart/", views.CartView.as_view(), name="cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove-from-cart"),
    path("cart/checkout/", views.checkout, name="checkout"),
    path("cart/order-completed/", views.OrderSuccessView.as_view(), name="order-completed"),
    path("cart/order-history/", views.OrderListView.as_view(), name="order-history"),
]

