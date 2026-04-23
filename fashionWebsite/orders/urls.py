from django.urls import path, include

from fashionWebsite.orders import views

urlpatterns = [
    path("cart/", include([
        path("add/<int:garment_id>/", views.add_to_cart, name="add-to-cart"),
        path("", views.CartView.as_view(), name="cart"),
        path("remove/<int:item_id>/", views.remove_from_cart, name="remove-from-cart"),
        path("checkout/", views.checkout, name="checkout"),
        path("order-completed/", views.OrderSuccessView.as_view(), name="order-completed"),
        path("order-history/", views.OrderListView.as_view(), name="order-history"),
        path("update-profile/", views.update_customer_form_cart, name="update-customer-from-cart"),
        path("apply-promo/", views.apply_promo_code, name="apply-promo-code"),
    ])),

    path("stripe/", include([
        path("checkout/", views.create_stripe_checkout, name="stripe-checkout"),
        path("webhook/", views.stripe_webhook, name="stripe-webhook"),
    ])),
]

