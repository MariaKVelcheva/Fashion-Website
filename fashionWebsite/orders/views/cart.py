from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, TemplateView

from fashionWebsite.clothes.models import Product, Garment
from fashionWebsite.orders.models import OrderItem, Order

from fashionWebsite.orders.utils import get_or_create_cart, update_order_total


def add_to_cart(request, garment_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    color_id = request.POST.get("color")
    size_id = request.POST.get("size")

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
        return redirect("details-garment", slug=product.garment.slug)

    order = get_or_create_cart(request.user)

    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        product=product,
        defaults={
            "quantity": 1,
            "unit_price": product.garment.price,
            "promotion": None,
        }
    )

    if not created:
        if order_item.quantity + 1 > product.stock:
            messages.error(request, "Not enough stock available.")
            return redirect("details-garment", pk=garment_id)

        order_item.quantity += 1
        order_item.save()

    update_order_total(order)
    return redirect("details-garment", pk=garment_id)


class CartView(TemplateView):
    template_name = "orders/orders/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            order = get_or_create_cart(self.request.user)
            context["items"] = order.items.all()
            context["order"] = order
            context["session_cart"] = False
        else:
            cart = self.request.session.get("cart", {})
            items = []
            total = 0

            for product_id, quantity in cart.items():
                try:
                    product = Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                    continue

                item_total = product.garment.price * quantity
                total += item_total

                items.append({
                    "product": product,
                    "quantity": quantity,
                    "unit_price": product.garment.price,
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
        cart = request.session.get("cart", {})
        cart.pop(str(item_id), None)
        request.session["cart"] = cart
        return JsonResponse({
            "success": True,
            "cart_count": sum(cart.values()),
            "item_id": item_id,
      })

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

    for item in order.items.all():
        if item.product.stock < item.quantity:
            messages.error(request, "Sorry, only {item.product.stock} unit(s)"
                                    " of {item.product.garment.name} are available.")
            return redirect("cart")

    for item in order.items.all():
        item.product.stock -= item.quantity
        item.product.save()

    customer = request.user.customer
    order.shipping_address = request.POST.get("address") or customer.address
    order.phone_number = request.POST.get("phone") or customer.phone
    order.status = "confirmed"

    order.save()

    return redirect("order-completed")


class OrderSuccessView(TemplateView):
    template_name = "orders/orders/success.html"