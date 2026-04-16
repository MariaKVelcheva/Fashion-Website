from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView, TemplateView

from fashionWebsite.accounts.forms import UpdateCustomerForm
from fashionWebsite.clothes.models import Product, Garment
from fashionWebsite.orders.models import OrderItem, Order

from fashionWebsite.orders.utils import get_or_create_cart, update_order_total


def add_to_cart(request, garment_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request."}, status=400)

    garment = get_object_or_404(Garment, id=garment_id)

    color_id = request.POST.get("color")
    size_id = request.POST.get("size")

    available_products = Product.objects.filter(garment=garment, stock__gt=0)

    if not color_id:
        colors = available_products.values_list("color_id", flat=True).distinct()
        if colors.count() == 1:
            color_id = colors.first()
        else:
            return JsonResponse({"error": "Please select a colour."}, status=400)

    if not size_id:
        sizes = available_products.filter(color_id=color_id).values_list("size_id", flat=True).distinct()
        if sizes.count() == 1:
            size_id = sizes.first()
        else:
            return JsonResponse({"error": "Please select a size."}, status=400)

    product = get_object_or_404(
        Product,
        garment=garment,
        color_id=color_id,
        size_id=size_id,
    )

    if product.stock < 1:
        return JsonResponse({"error": "This item is out of stock."}, status=400)

    if not request.user.is_authenticated:
        cart = request.session.get("cart", {})
        product_id = str(product.id)
        cart[product_id] = cart.get(product_id, 0) + 1
        request.session["cart"] = cart
        return JsonResponse({
            "success": True,
            "message": "Added to cart!",
        })

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
            return JsonResponse({"error": "Not enough stock available."}, status=400)
        order_item.quantity += 1
        order_item.save()

    update_order_total(order)
    return JsonResponse({
        "success": True,
        "message": "Added to cart!",
    })

class CartView(TemplateView):
    template_name = "orders/orders/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        free_delivery_threshold = 60
        current_total = 0

        if self.request.user.is_authenticated:
            order = get_or_create_cart(self.request.user)
            current_total = order.total_amount
            context["items"] = order.items.all()
            context["order"] = order
            context["session_cart"] = False

            customer = self.request.user.customer
            profile_complete = customer.is_profile_complete()
            context["profile_complete"] = profile_complete
            context["customer_form"] = UpdateCustomerForm(instance=customer)

        else:
            cart = self.request.session.get("cart", {})
            items = []

            for product_id, quantity in cart.items():
                try:
                    product = Product.objects.select_related(
                        "garment", "color", "size"
                    ).get(id=product_id)
                except Product.DoesNotExist:
                    continue

                item_total = product.garment.price * quantity
                current_total += item_total

                items.append({
                    "product": product,
                    "quantity": quantity,
                    "unit_price": product.garment.price,
                    "line_total": item_total,
                })

            context["items"] = items
            context["total"] = current_total
            context["session_cart"] = True

        gap = free_delivery_threshold - current_total
        context["delivery_gap"] = gap if gap > 0 else None
        return context


def remove_from_cart(request, item_id):
    if request.method != "POST":
        return redirect("cart")

    if not request.user.is_authenticated:
        cart = request.session.get("cart", {})
        product_id = str(item_id)
        cart.pop(str(item_id), None)
        request.session["cart"] = cart
        return redirect("cart")

    item = get_object_or_404(OrderItem, id=item_id)

    if item.order.customer != request.user:
        return redirect("cart")

    order = item.order
    item.delete()
    update_order_total(order)
    return redirect("cart")


@login_required
def update_customer_form_cart(request):
    if request.method != "POST":
        return redirect("cart")

    customer = request.user.customer
    form = UpdateCustomerForm(request.POST, instance=customer)

    if form.is_valid():
        form.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("cart")

    order = get_or_create_cart(request.user)
    return render(request, "orders/orders/cart.html", {
        "items": order.items.all(),
        "order": order,
        "session_cart": False,
        "profile_complete": False,
        "customer_form": form,  # form with errors
        "delivery_gap": max(0, 60 - order.total_amount) or None,
    })


def checkout(request):
    if request.method != "POST":
        return redirect("cart")

    if not request.user.is_authenticated:
        return redirect("login")

    if not request.user.customer.is_profile_complete():
        messages.error(request, "Please complete your profile before checking out.")
        return redirect("cart")

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
    order.phone_number = request.POST.get("phone") or customer.telephone_number
    order.status = "confirmed"

    order.save()

    return redirect("order-completed")


class OrderSuccessView(TemplateView):
    template_name = "orders/orders/success.html"

