from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from fashionWebsite.clothes.models import Garment
from fashionWebsite.orders.models import OrderItem
from fashionWebsite.reviews.forms import ReviewForm, UpdateReviewForm
from fashionWebsite.reviews.models import Review


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "clothes/garments/details-garment.html"

    def form_valid(self, form):
        garment = get_object_or_404(Garment, slug=self.kwargs["slug"])

        if Review.objects.filter(
            garment=garment,
            user=self.request.user,
        ).exists():
            messages.error(self.request, "You have already reviewed this product.")
            return redirect(reverse("details-garment", kwargs={"slug": garment.slug}))

        review = form.save(commit=False)

        review.garment = garment
        review.user = self.request.user
        review.status = Review.PENDING
        review.verified_purchase = OrderItem.objects.filter(
            order__customer=self.request.user,
            order__status="received",
            product__garment=garment,
        ).exists()
        review.save()
        messages.success(self.request, "Thank you for your review. It will appear once approved.")

        return redirect(reverse("details-garment", kwargs={"slug": garment.slug}))

    def form_invalid(self, form):
        messages.error(self.request, "Please, write a valid review.")
        return redirect(reverse("details-garment", kwargs={"slug": self.kwargs["slug"]}))


class UpdateReviewView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = UpdateReviewForm
    template_name = "reviews/update-review.html"

    def form_valid(self, form):
        review = form.save(commit=False)
        review.status = Review.PENDING
        review.save()

        messages.success(self.request, "Your review update has been submitted for approval.")

        return redirect(reverse("details-garment", kwargs={"slug": review.garment.slug}))

    def dispatch(self, request, *args, **kwargs):
        review = self.get_object()

        if review.user != request.user and not request.user.is_superuser:
            messages.error(request, "This is another customer's review - you cannot change it.")
            return redirect(reverse("details-garment", kwargs={"slug": review.garment.slug}))

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("details-garment", kwargs={"slug": self.object.garment.slug})


class DeleteReviewView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = "reviews/delete-review.html"

    def dispatch(self, request, *args, **kwargs):
        review = self.get_object()
        if review.user != request.user and not request.user.is_superuser:
            messages.error(request, "This is another customer's review - you can't delete it.")
            return redirect(reverse("details-garment", kwargs={"slug": review.garment.slug}))

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("details-garment", kwargs={"slug": self.object.garment.slug})



