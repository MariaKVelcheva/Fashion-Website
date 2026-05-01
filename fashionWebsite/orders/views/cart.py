import stripe

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from fashionWebsite.promotions.models import Promotion
from fashionWebsite.accounts.forms import UpdateCustomerForm
from fashionWebsite.clothes.models import Product, Garment
from fashionWebsite.orders.models import OrderItem, Order
from fashionWebsite.orders.utils import get_or_create_cart, update_order_total
from fashionWebsite.common.tasks import send_email_task

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required(login_url="login")
def apply_promo_code(request):
    if request.method != "POST":
        return JsonResponse({"error": _("Invalid request")}, status=400)

    promo_code = request.POST.get("promo_code")

    promotion = Promotion.objects.filter(code=promo_code, type="code").first()

    if promotion is None:
        return JsonResponse({"error": _("Promotion not found")}, status=400)

    if promotion.is_valid:
        order = get_or_create_cart(request.user)

        if order.promotion:
            return JsonResponse({"error": _("A promo code is already applied to your order.")}, status=400)

        if promotion.min_order_amount and order.total_amount < promotion.min_order_amount:
            return JsonResponse({"error": _("Minimum order amount not reached")}, status=400)

        order.promotion = promotion
        promotion.times_used += 1
        order.total_amount = promotion.apply_to_order(order)
        promotion.save()
        order.save()

        return JsonResponse({
            "success": True,
            "message": _("Promo code applied!"),
            "new_total": str(order.total_amount),
        })
    else:
        return JsonResponse({"error": _("Invalid request")}, status=400)


def add_to_cart(request, garment_id):
    try:
        if request.method != "POST":
            return JsonResponse({"error": _("Invalid request.")}, status=400)

        garment = get_object_or_404(Garment, id=garment_id)

        color_id = request.POST.get("color")
        size_id = request.POST.get("size")

        available_products = Product.objects.filter(garment=garment, stock__gt=0)

        if not color_id:
            colors = available_products.values_list("color_id", flat=True).distinct()
            if colors.count() == 1:
                color_id = colors.first()
            else:
                return JsonResponse({"error": _("Please select a color.")}, status=400)

        if not size_id:
            sizes = available_products.filter(color_id=color_id).values_list("size_id", flat=True).distinct()
            if sizes.count() == 1:
                size_id = sizes.first()
            else:
                return JsonResponse({"error": _("Please select a size.")}, status=400)

        product = get_object_or_404(
            Product,
            garment=garment,
            color_id=color_id,
            size_id=size_id,
        )

        if product.stock < 1:
            return JsonResponse({"error": _("This item is out of stock.")}, status=400)

        if not request.user.is_authenticated:
            cart = request.session.get("cart", {})
            product_id = str(product.id)
            cart[product_id] = cart.get(product_id, 0) + 1
            request.session["cart"] = cart
            return JsonResponse({
                "success": True,
                "message": _("Added to cart!"),
                "cart_count": sum(cart.values()),
            })

        order = get_or_create_cart(request.user)

        order_item, created = OrderItem.objects.get_or_create(
            order=order,
            product=product,
            defaults={
                "quantity": 1,
                "unit_price": product.garment.discounted_price or product.garment.price,
            }
        )

        if not created:
            if order_item.quantity + 1 > product.stock:
                return JsonResponse({"error": _("Not enough stock available.")}, status=400)
            order_item.quantity += 1
            order_item.save()

        update_order_total(order)
        cart_count = sum(i.quantity for i in order.items.all())

        return JsonResponse({
            "success": True,
            "message": _("Added to cart!"),
            "cart_count": cart_count,
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)


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
        messages.success(request, _("Profile updated successfully."))
        return redirect("cart")

    order = get_or_create_cart(request.user)
    return render(request, "orders/orders/cart.html", {
        "items": order.items.all(),
        "order": order,
        "session_cart": False,
        "profile_complete": False,
        "customer_form": form,
        "delivery_gap": max(0, 60 - order.total_amount) or None,
    })


def checkout(request):
    if request.method != "POST":
        return redirect("cart")

    if not request.user.is_authenticated:
        return redirect("login")

    if not request.user.customer.is_profile_complete():
        messages.error(request, _("Please complete your profile before checking out."))
        return redirect("cart")

    order = get_or_create_cart(request.user)

    if not order.items.exists():
        messages.error(request, _("Your cart is empty."))
        return redirect("cart")

    for item in order.items.all():
        if item.product.stock < item.quantity:
            messages.error(
                request,
                _(f"Sorry, only {item.product.stock} unit(s) of "
                  f"{item.product.garment.name} are available.")
            )
            return redirect("cart")

    for item in order.items.all():
        item.product.stock -= item.quantity
        item.product.save()

    customer = request.user.customer

    order.shipping_address = request.POST.get("address") or customer.address
    order.phone_number = request.POST.get("phone") or customer.telephone_number

    order.payment_type = request.POST.get("payment_type", "pod")

    order.status = "confirmed"
    order.save()

    send_email_task.delay(
        subject=_("EllaPrimE - Order confirmation #%(order_id)s") % {
            "order_id": order.id
        },
        template_name="emails/order_confirmation.html",
        context={
            "order_id": order.id,
            "user_email": request.user.email,
            "items": [
                {
                    "name": item.product.garment.name,
                    "size": item.product.size.name,
                    "color": item.product.color.name,
                    "quantity": item.quantity,
                    "unit_price": str(item.unit_price),
                    "line_total": str(item.line_total),
                }
                for item in order.items.all()
            ],
            "total_amount": str(order.total_amount),
            "shipping_address": order.shipping_address,
            "phone_number": order.phone_number,
            "payment_type": order.get_payment_type_display(),
        },
        recipient_list=[request.user.email],
    )

    send_email_task.delay(
        subject=f"New order #{order.id} — {request.user.email}",
        template_name="emails/admin_order_notification.html",
        context={
            "order_id": order.id,
            "user_email": request.user.email,
            "customer_name": customer.full_name,
            "items": [
                {
                    "name": item.product.garment.name,
                    "size": item.product.size.name,
                    "color": item.product.color.name,
                    "quantity": item.quantity,
                    "unit_price": str(item.unit_price),
                    "line_total": str(item.line_total),
                }
                for item in order.items.all()
            ],
            "total_amount": str(order.total_amount),
            "shipping_address": order.shipping_address,
            "phone_number": order.phone_number,
            "payment_type": order.get_payment_type_display(),
        },
        recipient_list=[settings.DEFAULT_FROM_EMAIL],
    )

    points_earned = int(order.total_amount)
    request.user.loyalty_points += points_earned
    request.user.save()

    return redirect("order-completed")


class OrderSuccessView(TemplateView):
    template_name = "orders/orders/success.html"


def create_stripe_checkout(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if not request.user.customer.is_profile_complete():
        messages.error(request, _("Please complete your profile before checking out."))
        return redirect("cart")

    order = get_or_create_cart(request.user)

    if not order.items.exists():
        messages.error(request, _("Your cart is empty."))
        return redirect("cart")

    for item in order.items.all():
        if item.product.stock < item.quantity:
            messages.error(
                request,
                _("Sorry, only %(stock)s unit(s) of %(name)s are available.") % {
                    "stock": item.product.stock,
                    "name": item.product.garment.name,
                }
            )
            return redirect("cart")

    line_items = []
    for item in order.items.all():
        line_items.append({
            "price_data": {
                "currency": "eur",
                "unit_amount": int(item.unit_price * 100),  # Stripe uses cents
                "product_data": {
                    "name": item.product.garment.name,
                    "description": f"{item.product.size.name} / {item.product.color.name}",
                },
            },
            "quantity": item.quantity,
        })

    customer = request.user.customer
    order.shipping_address = customer.address
    order.phone_number = customer.telephone_number
    order.payment_type = "card"
    order.save()

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=request.build_absolute_uri("/orders/cart/order-completed/"),
        cancel_url=request.build_absolute_uri("/orders/cart/"),
        metadata={
            "order_id": order.id,
            "user_id": request.user.id,
        },
        customer_email=request.user.email,
    )

    return redirect(session.url, code=303)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        order_id = session["metadata"].get("order_id")

        try:
            order = Order.objects.get(id=order_id, status="pending")
        except Order.DoesNotExist:
            return HttpResponse(status=200)

        for item in order.items.all():
            item.product.stock -= item.quantity
            item.product.save()

        order.status = "confirmed"
        User = get_user_model()
        user = User.objects.get(id=order.customer.id)
        user.loyalty_points += int(order.total_amount)
        user.save()
        order.save()

        send_email_task.delay(
            subject=_("EllaPrimE - Order confirmation #%(order_id)s") % {
                "order_id": order_id,
            },
            template_name="emails/order_confirmation.html",
            context={
                "order_id": order.id,
                "user_email": order.customer.email,
                "items": [
                    {
                        "name": item.product.garment.name,
                        "size": item.product.size.name,
                        "color": item.product.color.name,
                        "quantity": item.quantity,
                        "unit_price": str(item.unit_price),
                        "line_total": str(item.line_total),
                    }
                    for item in order.items.all()
                ],
                "total_amount": str(order.total_amount),
                "shipping_address": order.shipping_address,
                "phone_number": order.phone_number,
                "payment_type": order.get_payment_type_display(),
            },
            recipient_list=[order.customer.email],
        )

        send_email_task.delay(
            subject=f"New order #{order.id} — {order.customer.email}",
            template_name="emails/admin_order_notification.html",
            context={
                "order_id": order.id,
                "user_email": order.customer.email,
                "customer_name": order.customer.customer.full_name,
                "items": [
                    {
                        "name": item.product.garment.name,
                        "size": item.product.size.name,
                        "color": item.product.color.name,
                        "quantity": item.quantity,
                        "unit_price": str(item.unit_price),
                        "line_total": str(item.line_total),
                    }
                    for item in order.items.all()
                ],
                "total_amount": str(order.total_amount),
                "shipping_address": order.shipping_address,
                "phone_number": order.phone_number,
                "payment_type": order.get_payment_type_display(),
            },
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
        )

    return HttpResponse(status=200)


