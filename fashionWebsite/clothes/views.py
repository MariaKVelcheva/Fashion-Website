from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView

from fashionWebsite.clothes.forms import CreateGarmentForm, UpdateGarmentForm, DeleteGarmentForm, CreateColorForm, \
    CreateSizeForm, CreateCategoryForm, UpdateCategoryForm, ProductFormSet
from fashionWebsite.clothes.models import Garment, Color, Size, Category, GarmentImage, WishlistItem, Product
from fashionWebsite.common.mixins import AdminRequiredMixin
from django.http import JsonResponse


class CreateGarmentView(AdminRequiredMixin, CreateView):
    model = Garment
    form_class = CreateGarmentForm
    template_name = "clothes/garments/create-garment.html"

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]

        if formset.is_valid():
            self.object = form.save()
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["images"] = self.object.images.all()
        if self.request.user.is_authenticated:
            wishlist_ids = WishlistItem.objects.filter(
                user=self.request.user
            ).values_list('garment_id', flat=True)

            context['user_wishlist'] = list(wishlist_ids)
        else:
            context['user_wishlist'] = []
        return context


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
        return Garment.objects.filter(products__stock__gt=0).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            wishlist_ids = WishlistItem.objects.filter(
                user=self.request.user
            ).values_list('garment_id', flat=True)

            context['user_wishlist'] = list(wishlist_ids)
        else:
            context['user_wishlist'] = []

        return context


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


class GarmentSearchView(ListView):
    model = Garment
    template_name = 'clothes/garments/search.html'
    context_object_name = 'garments'

    def get_queryset(self):
        queryset = Garment.objects.filter(products__stock__gt=0).distinct()

        q = self.request.GET.get('q')

        category_ids = self.request.GET.getlist('category')
        color_ids = self.request.GET.getlist('color')
        size_ids = self.request.GET.getlist('size')

        query = Q()

        if q:
            query |= Q(name__icontains=q)
            query |= Q(description__icontains=q)

        if category_ids:
            query |= Q(category_id__in=category_ids)

        if color_ids:
            query |= Q(products__color_id__in=color_ids)

        if size_ids:
            query |= Q(products__size_id__in=size_ids)

        if query:
            queryset = queryset.filter(query)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['colors'] = Color.objects.all()
        context['sizes'] = Size.objects.all()

        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_color'] = self.request.GET.get('color', '')
        context['selected_size'] = self.request.GET.get('size', '')

        context['q'] = self.request.GET.get('q', '')

        return context


@login_required
def toggle_wishlist(request, garment_id):
    garment = get_object_or_404(Garment, id=garment_id)

    item, created = WishlistItem.objects.get_or_create(
        user=request.user,
        garment=garment
    )

    if not created:
        item.delete()
        status = 'removed'
    else:
        status = 'added'

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': status, 'garment_id': garment.id})

    return redirect(request.META.get('HTTP_REFERER', 'home'))


class CategoryDetailView(ListView):
    model = Garment
    template_name = 'clothes/categories/details-category.html'
    context_object_name = 'garments'

    def get_queryset(self):
        category_pk = self.kwargs.get('slug')
        self.category = get_object_or_404(Category, pk=category_pk)

        # filter garments for this category
        return Garment.objects.filter(category=self.category, products__stock__gt=0).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['garments'] = self.get_queryset()
        return context


