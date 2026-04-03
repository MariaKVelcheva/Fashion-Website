from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, ListView, TemplateView
from django.urls import reverse_lazy

from fashionWebsite.clothes.models import Product
from fashionWebsite.common.mixins import AdminRequiredMixin
from fashionWebsite.orders.forms import CreatePromotionForm, UpdatePromotionForm
from fashionWebsite.orders.models import Promotion, OrderItem, Order
from django.contrib.auth.mixins import LoginRequiredMixin

from fashionWebsite.orders.utils import get_or_create_cart, update_order_total


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


def add_to_cart(request, garment_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    color_id = request.POST.get("color")
    size_id = request.POST.get("size")

    if not color_id or not size_id:
        if not color_id or not size_id:
            return JsonResponse({"error": "Please select size and color."}, status=400)

    product = get_object_or_404(
        Product,
        garment_id=garment_id,
        color_id=color_id,
        size_id=size_id
    )

    if product.stock < 1:
        return JsonResponse({"error": "Out of stock"}, status=400)

    if not request.user.is_authenticated:
        cart = request.session.get("cart", {})

        product_id = str(product.id)

        if product_id in cart:
            cart[product_id] += 1
        else:
            cart[product_id] = 1

        request.session["cart"] = cart
        return JsonResponse({
            "success": True,
            "message": "Added to cart",
            "cart_count": sum(cart.values())
        })

    order = get_or_create_cart(request.user)

    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        product=product,
        defaults={
            "quantity": 1,
            "unit_price": product.garment.price,
        }
    )

    if not created:
        if order_item.quantity + 1 > product.stock:
            messages.error(request, "Not enough stock available.")
            return redirect("garment-detail", pk=garment_id)

        order_item.quantity += 1
        order_item.save()

    update_order_total(order)

    return redirect("garment-detail", pk=garment_id)


class CartView(TemplateView):
    template_name = "orders/orders/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🟢 Logged-in user
        if self.request.user.is_authenticated:
            order = get_or_create_cart(self.request.user)
            context["items"] = order.items.all()
            context["order"] = order
            context["session_cart"] = False

        # 🔵 Anonymous user
        else:
            cart = self.request.session.get("cart", {})
            items = []
            total = 0

            for product_id, quantity in cart.items():
                product = Product.objects.get(id=product_id)

                item_total = product.price * quantity
                total += item_total

                items.append({
                    "product": product,
                    "quantity": quantity,
                    "unit_price": product.price,
                    "line_total": item_total,
                })

            context["items"] = items
            context["total"] = total
            context["session_cart"] = True

        return context


def remove_from_cart(request, item_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required"}, status=403)
    item = get_object_or_404(OrderItem, id=item_id)

    if item.order.customer != request.user:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    order = item.order
    item.delete()

    update_order_total(order)

    cart_count = sum(i.quantity for i in order.items.all())

    return JsonResponse({
        "success": True,
        "cart_count": cart_count,
        "item_id": item_id
    })


def checkout(request):
    if request.method != "POST":
        return redirect("cart")

    if not request.user.is_authenticated:
        return redirect("login")

    order = get_or_create_cart(request.user)

    if not order.items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("cart")

    try:
        customer = request.user.customer
    except:
        messages.error(request, "Please complete your profile first.")
        return redirect("cart")

    for item in order.items.all():
        if item.product.stock < item.quantity:
            messages.error(request, "Not enough stock")
            return redirect("cart")

    for item in order.items.all():
        item.product.stock -= item.quantity
        item.product.save()

    order.shipping_address = request.POST.get("address")
    order.phone_number = request.POST.get("phone")
    order.status = "confirmed"
    customer = get_user_model().customer

    order.shipping_address = customer.address
    order.phone_number = customer.phone_number
    order.save()
    order.save()

    return redirect("order-success")


class OrderSuccessView(TemplateView):
    template_name = "orders/orders/success.html"


class OrderListView(ListView):
    model = Order
    template_name = "orders/orders/all-orders.html"

    def get_queryset(self):
        return Order.objects.filter(
            customer=self.request.user
        ).exclude(status="pending")

