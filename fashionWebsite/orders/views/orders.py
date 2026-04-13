from django.views.generic import ListView, TemplateView
from fashionWebsite.orders.models import Order


class OrderSuccessView(TemplateView):
    template_name = "orders/orders/success.html"


class OrderListView(ListView):
    model = Order
    template_name = "orders/orders/all-orders.html"

    def get_queryset(self):
        return Order.objects.filter(
            customer=self.request.user
        ).exclude(status="pending")

