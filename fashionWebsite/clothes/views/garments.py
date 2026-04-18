from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Case, When, IntegerField
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import DetailView, ListView
from fashionWebsite.clothes.models import Garment, Color, Size, Category, WishlistItem, LookbookImage
from django.http import JsonResponse


@login_required
def toggle_wishlist(request, garment_id):
    try:
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
        return JsonResponse({'status': status, 'garment_id': garment.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


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
        queryset = Garment.objects.all().annotate(
            in_stock=Case(
                When(products__stock__gt=0, then=0),
                default=1,
                output_field=IntegerField(),
            )
        ).order_by("in_stock", "name").distinct()

        q = self.request.GET.get('q')
        category_ids = self.request.GET.getlist('category')
        color_ids = self.request.GET.getlist('color')
        size_ids = self.request.GET.getlist('size')

        if q:
            q_singular = q.rstrip('s') if q.endswith('s') and len(q) > 2 else q
            queryset = queryset.filter(
                Q(name__icontains=q) |
                Q(description__icontains=q) |
                Q(name__icontains=q_singular) |
                Q(description__icontains=q_singular) |
                Q(category__name__icontains=q)
            )

        if category_ids:
            queryset = queryset.filter(category__id__in=category_ids)

        if color_ids:
            queryset = queryset.filter(products__color_id__in=color_ids)

        if size_ids:
            queryset = queryset.filter(products__size_id__in=size_ids)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['colors'] = Color.objects.all()
        context['sizes'] = Size.objects.all()

        context['selected_categories'] = self.request.GET.getlist('category')
        context['selected_colors'] = self.request.GET.getlist('color')
        context['selected_sizes'] = self.request.GET.getlist('size')

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
        queryset = Garment.objects.all().annotate(
            in_stock=Case(
                When(products__stock__gt=0, then=0),
                default=1,
                output_field=IntegerField(),
            )
        ).order_by("in_stock", "name").distinct()
        return queryset

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
    context_object_name = "garments"

    def get_queryset(self):
        newest = timezone.now() - timedelta(days=60)
        return Garment.objects.filter(
            created_at__gte=newest
        ).prefetch_related("category").annotate(
            in_stock=Case(
                When(products__stock__gt=0, then=0),
                default=1,
                output_field=IntegerField(),
            )
        ).order_by("in_stock", "name").distinct()


class TrendingView(ListView):
    model = Garment
    context_object_name = "garments"

    def get_queryset(self):
        queryset = Garment.objects.filter(category__trending=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.filter(trending=True).first()
        return context


class GalleryView(ListView):
    model = LookbookImage
    template_name = "common/gallery.html"
    context_object_name = "images"
    queryset = LookbookImage.objects.all()


