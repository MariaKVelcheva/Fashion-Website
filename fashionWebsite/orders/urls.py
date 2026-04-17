from django.urls import path, include

from fashionWebsite.orders import views

urlpatterns = [
    path("cart/add/<int:garment_id>/", views.add_to_cart, name="add-to-cart"),
    path("cart/", views.CartView.as_view(), name="cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove-from-cart"),
    path("cart/checkout/", views.checkout, name="checkout"),

    path("cart/order-completed/", views.OrderSuccessView.as_view(), name="order-completed"),
    path("cart/order-history/", views.OrderListView.as_view(), name="order-history"),
    path("cart/update-profile/", views.update_customer_form_cart, name="update-customer-from-cart"),
    path("stripe/checkout/", views.create_stripe_checkout, name="stripe-checkout"),
    path("stripe/webhook/", views.stripe_webhook, name="stripe-webhook"),
]

