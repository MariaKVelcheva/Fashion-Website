from urllib.parse import urlparse

from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy

from fashionWebsite.accounts.forms import AppUserCreationForm, LoginForm, UpdateCustomerForm
from fashionWebsite.accounts.models import Customer

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
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)

        return response


class LoginUserView(LoginView):
    model = AppUser
    form_class = LoginForm
    template_name = "accounts/user-management/login.html"


class LogoutUserView(LogoutView):
    pass


class UpdateCustomerView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = UpdateCustomerForm
    template_name = "accounts/profile-management/customer-update.html"
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        customer, created = Customer.objects.get_or_create(user=self.request.user)
        return customer


class DetailsCustomerView(LoginRequiredMixin, DetailView):
    model = Customer
    context_object_name = "customer"
    template_name = "accounts/profile-management/customer-details.html"

    def get_object(self, queryset=None):
        customer, created = Customer.objects.get_or_create(user=self.request.user)
        return customer
