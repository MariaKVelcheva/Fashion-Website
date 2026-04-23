from django.contrib import admin
from fashionWebsite.promotions.models import Promotion


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ("code", "type", "discount_percent", )
    list_filter = ("type", )

