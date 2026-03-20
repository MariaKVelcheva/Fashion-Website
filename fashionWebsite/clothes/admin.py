from django.contrib import admin
from fashionWebsite.clothes.models import Category, Size, Color, Garment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", )
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ("name", )


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ("name", "hex_code")
    list_editable = ("hex_code", )


@admin.register(Garment)
class GarmentAdmin(admin.ModelAdmin):
    list_display = ("name", "category__name", "price", "color__name", "size__name", "stock", "discount_price")
    list_filter = ("category__name", )

