from django.contrib import admin
from fashionWebsite.orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ("product", "quantity", "unit_price", "line_total")
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ("id", "customer", "status", "total_amount", "created_at")
    list_filter = ("status",)
    list_editable = ("status",)
    readonly_fields = ("created_at", "total_amount")
    ordering = ("-created_at",)


