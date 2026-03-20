from django.contrib import admin
from fashionWebsite.orders.models import Order, Promotion, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ("status", "payment_type", "total_amount")
    list_filter = ("status", "payment_type", "created_at", "customer__email")
    raw_id_fields = ("customer", )


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ("code", "type", "discount_percent", )
    list_filter = ("type", )

