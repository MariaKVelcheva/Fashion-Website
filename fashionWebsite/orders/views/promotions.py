from fashionWebsite.common.mixins import AdminRequiredMixin
from fashionWebsite.orders.forms import CreatePromotionForm, UpdatePromotionForm
from fashionWebsite.orders.models import Promotion, OrderItem, Order
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, ListView, TemplateView
from django.urls import reverse_lazy


class CreatePromotionView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Promotion
    form_class = CreatePromotionForm
    success_url = reverse_lazy("all-promotions")
    template_name = "orders/promotions/create-promotion.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["promotions"] = Promotion.objects.all()
        return context


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
        return Promotion.objects.all().order_by('-valid_until')
