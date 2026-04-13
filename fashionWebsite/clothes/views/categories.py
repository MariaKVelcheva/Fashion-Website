from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from fashionWebsite.clothes.forms import CreateGarmentForm, UpdateGarmentForm, DeleteGarmentForm, CreateColorForm, \
    CreateSizeForm, CreateCategoryForm, UpdateCategoryForm, ProductFormSet
from fashionWebsite.clothes.models import Garment, Color, Size, Category, GarmentImage, WishlistItem, Product
from fashionWebsite.common.mixins import AdminRequiredMixin


class CreateCategoryView(AdminRequiredMixin, CreateView):
    model = Category
    form_class = CreateCategoryForm
    template_name = "clothes/categories/create-category.html"
    success_url = reverse_lazy("all-categories")

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class UpdateCategoryView(AdminRequiredMixin, UpdateView):
    model = Category
    form_class = UpdateCategoryForm
    slug_url_kwarg = "slug"
    slug_field = "slug"
    template_name = "clothes/categories/update-category.html"
    success_url = reverse_lazy("all-categories")


class DeleteCategoryView(AdminRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy("all-categories")


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
        self.category = get_object_or_404(Category, pk=category_pk)

        return Garment.objects.filter(category=self.category, products__stock__gt=0).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['garments'] = self.get_queryset()
        return context


