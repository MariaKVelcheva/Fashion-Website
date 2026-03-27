from django.views.generic import CreateView, UpdateView, ListView
from django.urls import reverse_lazy

from fashionWebsite.common.mixins import AdminRequiredMixin
from fashionWebsite.orders.forms import CreatePromotionForm, UpdatePromotionForm
from fashionWebsite.orders.models import Promotion
from django.contrib.auth.mixins import LoginRequiredMixin


class CreatePromotionView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Promotion
    form_class = CreatePromotionForm
    success_url = reverse_lazy("all-promotions")
    template_name = "orders/promotions/create-promotion.html"


class UpdatePromotionView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Promotion
    form_class = UpdatePromotionForm
    success_url = reverse_lazy("all-promotions")
    template_name = "orders/promotions/update-promotion.html"


class PromotionsCatalogueView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Promotion
    template_name = "orders/promotions/all-promotions.html"
    context_object_name = "promotions"

    def get_queryset(self):
        return Promotion.objects.filter(is_active=True).order_by('-valid_until')



