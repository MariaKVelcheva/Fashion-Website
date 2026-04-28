from django.contrib import admin

from fashionWebsite.reviews.models import Review


@admin.action(description="Approve selected reviews")
def approve_reviews(modeladmin, request, queryset):
    queryset.update(status=Review.APPROVED)


@admin.action(description="Reject selected reviews")
def reject_reviews(modeladmin, request, queryset):
    queryset.update(status=Review.REJECTED)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("status", "garment", "rating", "created_at", "verified_purchase",)
    list_filter = ("created_at", "garment__name", "user__email",)
    ordering = ("created_at",)
    search_fields = ("garment__name", "status", "created_at", "user__email", )
    actions = [approve_reviews, reject_reviews]
