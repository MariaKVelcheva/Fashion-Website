from modeltranslation.translator import register, TranslationOptions
from fashionWebsite.clothes.models import Garment, Category


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)
    required_languages = ('en',)


@register(Garment)
class GarmentTranslationOptions(TranslationOptions):
    fields = ('name', 'description')