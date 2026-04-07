from urllib.parse import urlparse

from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy

from fashionWebsite.accounts.forms import AppUserCreationForm, LoginForm, UpdateCustomerForm
from fashionWebsite.accounts.models import Customer
from fashionWebsite.clothes.models import Product
from fashionWebsite.orders.models import OrderItem
from fashionWebsite.orders.utils import update_order_total, get_or_create_cart


AppUser = get_user_model()


class RegisterUserView(CreateView):
    model = AppUser
    form_class = AppUserCreationForm
    template_name = "accounts/user-management/register.html"

    def get_success_url(self):
        next_url = self.request.GET.get('next')

        if next_url:
            parsed_next = urlparse(next_url)
            if parsed_next.netloc == "":
                return next_url

        return reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        form.data = form.data.copy()
        form.data["email"] = ""
        return super().form_invalid(form)


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AppUser
    template_name = "accounts/user-management/confirm-delete.html"
    success_url = reverse_lazy("home")

    def post(self, request, *args, **kwargs):
        user = request.user
        user.is_active = False
        user.save()

        logout(request)

        messages.success(request, "Your account has been deleted.")
        return JsonResponse({"redirect_url": reverse_lazy("home")})


class LoginUserView(LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user
        self.merge_cart(user)
        return response

    def form_invalid(self, form):
        form.data = form.data.copy()
        form.data["email"] = ""
        return super().form_invalid(form)

    def merge_cart(self, user):
        cart = self.request.session.get("cart")
        if not cart:
            return
        order = get_or_create_cart(user)
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            order_item, created = OrderItem.objects.get_or_create(
                order=order,
                product=product,
                defaults={
                    "quantity": quantity,
                    "unit_price": product.price,
                }
            )
            if not created:
                order_item.quantity += quantity
                order_item.save()
        update_order_total(order)
        self.request.session["cart"] = {}


class LogoutUserView(LogoutView):
    next_page = reverse_lazy("home")


