from django.urls import path
from fashionWebsite.reviews import views


urlpatterns = [
    path("product/<slug:slug>/details/review/", views.ReviewCreateView.as_view(), name="review-create"),
    path("<int:pk>/update/", views.UpdateReviewView.as_view(), name="update-review"),
    path("<int:pk>/delete/", views.DeleteReviewView.as_view(), name="delete-review"),
]