from modeltranslation.admin import TranslationAdmin
from django.contrib import admin
from fashionWebsite.clothes.models import Category, Size, Color, Garment, Product, LookbookImage, GarmentImage


@admin.register(LookbookImage)
class LookbookImageAdmin(admin.ModelAdmin):
    list_display = ("__str__",)


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", )
    prepopulated_fields = {"slug": ("name_en",)}


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
    extra = 2
    autocomplete_fields = ("size", "color")


class GarmentImageInline(admin.TabularInline):
    model = GarmentImage
    extra = 3
    fields = ("image",)


@admin.register(Garment)
class GarmentAdmin(TranslationAdmin):
    inlines = [GarmentImageInline, ProductInline]
    prepopulated_fields = {"slug": ("name_en",)}
    list_display = ("name", "price", "is_available")
    search_fields = ("name", "price")
    list_filter = ("category",)

