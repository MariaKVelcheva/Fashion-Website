from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView

from fashionWebsite.clothes.forms import CreateGarmentForm, UpdateGarmentForm, DeleteGarmentForm, CreateColorForm, \
    CreateSizeForm, CreateCategoryForm, UpdateCategoryForm, ProductFormSet
from fashionWebsite.clothes.models import Garment, Color, Size, Category, GarmentImage
from fashionWebsite.common.mixins import AdminRequiredMixin


class CreateGarmentView(AdminRequiredMixin, CreateView):
    model = Garment
    form_class = CreateGarmentForm
    template_name = "clothes/garments/create-garment.html"

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]

        if formset.is_valid():
            self.object = form.save(commit=False)
            self.object.save()

            formset.instance = self.object
            formset.save()

            files = self.request.FILES.getlist("gallery_images")
            for file in files:
                GarmentImage.objects.create(
                    garment=self.object,
                    image=file
                )

            return redirect(self.get_success_url())

        return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("details-garment", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context["formset"] = ProductFormSet(self.request.POST)
        else:
            context["formset"] = ProductFormSet()

        return context


class DetailsGarmentView(DetailView):
    model = Garment
    slug_field = 'slug'
    slug_url_kwarg = "slug"
    template_name = "clothes/garments/details-garment.html"


class UpdateGarmentView(AdminRequiredMixin, UpdateView):
    model = Garment
    form_class = UpdateGarmentForm
    slug_url_kwarg = "slug"
    slug_field = "slug"
    template_name = "clothes/garments/update-garment.html"

    def get_success_url(self):
        return reverse_lazy("details-garment", kwargs={"pk": self.object.pk})


class DeleteGarmentView(AdminRequiredMixin, DeleteView):
    model = Garment
    form_class = DeleteGarmentForm
    slug_field = 'slug'
    slug_url_kwarg = "slug"
    template_name = "clothes/garments/delete-garment.html"
    success_url = reverse_lazy("all-garments")


class GarmentCatalogueView(ListView):
    model = Garment
    template_name = "clothes/garments/all-garments.html"
    context_object_name = "garments"

    def get_queryset(self):
        return Garment.objects.filter(is_available=True)


class CreateColorView(AdminRequiredMixin, CreateView):
    model = Color
    form_class = CreateColorForm
    template_name = "clothes/colors/create-color.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["colors"] = Color.objects.all()
        return context


class CreateSizeView(AdminRequiredMixin, CreateView):
    model = Size
    form_class = CreateSizeForm
    template_name = "clothes/sizes/create-size.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sizes"] = Size.objects.all()
        return context


class CreateCategoryView(AdminRequiredMixin, CreateView):
    model = Category
    form_class = CreateCategoryForm
    template_name = "clothes/categories/create-category.html"
    success_url = reverse_lazy("all-categories")

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


