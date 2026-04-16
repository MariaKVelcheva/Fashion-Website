from django.urls import path, include

from fashionWebsite.clothes import views

urlpatterns = [
    path("gallery/", views.GalleryView.as_view(), name="gallery"),
    path("new/", views.NewArrivalsView.as_view(), name="new"),
    path("all-categories/", views.CategoryCatalogueView.as_view(), name="all-categories"),
    path("all-products/", views.GarmentCatalogueView.as_view(), name="all-garments"),
    path("product/<slug:slug>/details/", views.DetailsGarmentView.as_view(), name="details-garment"),
    path("category/<slug:slug>/details/", views.CategoryDetailView.as_view(), name="details-category"),
    path('search/', views.GarmentSearchView.as_view(), name='garment-search'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle-wishlist'),
    path("wishlist/", views.WishlistView.as_view(), name="wishlist"),
]
