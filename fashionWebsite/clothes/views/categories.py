from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from fashionWebsite.clothes.models import Garment, Category


class CategoryCatalogueView(ListView):
    model = Category
    ordering = ("name", )
    template_name = "clothes/categories/all-categories.html"
    context_object_name = "categories"


class CategoryDetailView(ListView):
    model = Garment
    template_name = 'clothes/categories/details-category.html'
    context_object_name = 'garments'

    def get_queryset(self):
        category_pk = self.kwargs.get('slug')
        self.category = get_object_or_404(Category, slug=self.kwargs.get('slug'))

        return Garment.objects.filter(category=self.category, products__stock__gt=0).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['garments'] = self.get_queryset()
        return context


