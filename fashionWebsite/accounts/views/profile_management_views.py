from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, DetailView, FormView
from django.urls import reverse_lazy
from fashionWebsite.accounts.forms import UpdateCustomerForm
from fashionWebsite.accounts.models import Customer
from fashionWebsite.common.forms import ContactForm


class UpdateCustomerView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = UpdateCustomerForm
    template_name = "accounts/profile-management/customer-update.html"
    success_url = reverse_lazy("customer-details")

    def get_object(self, queryset=None):
        customer, created = Customer.objects.get_or_create(user=self.request.user)
        return customer

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully.")
        return super().form_valid(form)


class DetailsCustomerView(LoginRequiredMixin, DetailView, UpdateView, FormView):
    model = Customer
    form_class = UpdateCustomerForm
    context_object_name = "customer"
    template_name = "accounts/profile-management/customer-details.html"
    success_url = reverse_lazy("customer-details")

    def get_object(self, queryset=None):
        customer, created = Customer.objects.get_or_create(user=self.request.user)
        return customer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["orders"] = self.request.user.orders.all()
        context["contact_form"] = ContactForm()

        customer = self.get_object()
        context["profile_complete"] = customer.is_profile_complete()

        return context

