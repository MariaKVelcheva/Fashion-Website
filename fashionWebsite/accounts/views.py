from urllib.parse import urlparse

from django.contrib.auth import get_user_model, login
from django.views.generic import CreateView
from django.urls import reverse_lazy

from fashionWebsite.accounts.forms import AppUserCreationForm

AppUser = get_user_model()


class RegisterUserView(CreateView):
    model = AppUser
    form_class = AppUserCreationForm
    template_name = "accounts/user-management/register.html"

    def get_success_url(self):
        next_url = self.request.POST.get('next')

        if next_url:
            parsed_next = urlparse(next_url)
            if parsed_next.netloc == "":
                return next_url

        return reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        # user = form.save()
        login(self.request, user)

        return response

