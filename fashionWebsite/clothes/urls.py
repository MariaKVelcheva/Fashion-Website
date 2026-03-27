from django.urls import path, include

from fashionWebsite.clothes import views

urlpatterns = [
    path("all-categories/", views.CategoryCatalogueView.as_view(), name="all-categories"),
    path("all-products/", views.GarmentCatalogueView.as_view(), name="all-garments"),
    path("product/create/", views.CreateGarmentView.as_view(), name="create-garment"),
    path("product/<slug:slug>/", include([
        path("update/", views.UpdateGarmentView.as_view(), name="update-garment"),
        path("delete/", views.DeleteGarmentView.as_view(), name="delete-garment"),
        path("details/", views.DetailsGarmentView.as_view(), name="details-garment"),
    ])),
    path("color/create/", views.CreateColorView.as_view(), name="create-color"),
    path("size/create/", views.CreateSizeView.as_view(), name="create-size"),
    path("category/", include([
        path("create/", views.CreateCategoryView.as_view(), name="create-category"),
        path("<slug:slug>/update/", views.UpdateCategoryView.as_view(), name="update-category"),
        path("<slug:slug>/delete/", views.DeleteCategoryView.as_view(), name="delete-category"),
    ]))
]
