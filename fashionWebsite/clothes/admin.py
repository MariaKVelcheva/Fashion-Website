from django.contrib import admin
from fashionWebsite.clothes.models import Category, Size, Color, Garment, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", )
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ("name", )
    search_fields = ("name", )


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ("name", "hex_code")
    list_editable = ("hex_code", )
    search_fields = ("name", )


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1
    autocomplete_fields = ("size", "color")


@admin.register(Garment)
class GarmentAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
    list_display = ("name", "category__name", "price", "discount_price")
    search_fields = ("name", "category__name", "price", "discount_price", "size__name", "color__name")
    list_filter = ("category__name", )

