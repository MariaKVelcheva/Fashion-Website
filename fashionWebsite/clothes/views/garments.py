from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import DetailView, ListView
from fashionWebsite.clothes.models import Garment, Color, Size, Category, WishlistItem, LookbookImage
from django.http import JsonResponse


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


class WishlistView(LoginRequiredMixin, ListView):
    model = WishlistItem
    template_name = "clothes/garments/wishlist.html"
    context_object_name = "wishlist_items"

    def get_queryset(self):
        return (
            WishlistItem.objects
            .filter(user=self.request.user)
            .select_related("garment")
            .order_by("-created_at")
        )


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


class DetailsGarmentView(DetailView):
    model = Garment
    slug_field = 'slug'
    slug_url_kwarg = "slug"
    template_name = "clothes/garments/details-garment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["images"] = self.object.images.all()
        context["products"] = self.object.products.all()
        if self.request.user.is_authenticated:
            wishlist_ids = WishlistItem.objects.filter(
                user=self.request.user
            ).values_list('garment_id', flat=True)

            context['user_wishlist'] = list(wishlist_ids)
        else:
            context['user_wishlist'] = []
        return context


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


class NewArrivalsView(ListView):
    model = Garment
    template_name = "clothes/garments/new_in.html"

    def get_queryset(self):
        newest = timezone.now() - timedelta(days=60)
        return Garment.objects.filter(created_at__gte=newest)


class GalleryView(ListView):
    model = LookbookImage
    template_name = "common/gallery.html"
    context_object_name = "images"
    queryset = LookbookImage.objects.all()