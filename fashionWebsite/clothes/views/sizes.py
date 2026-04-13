from django.urls import reverse_lazy
from django.views.generic import CreateView
from fashionWebsite.clothes.forms import CreateSizeForm
from fashionWebsite.clothes.models import Size
from fashionWebsite.common.mixins import AdminRequiredMixin


class CreateSizeView(AdminRequiredMixin, CreateView):
    model = Size
    form_class = CreateSizeForm
    template_name = "clothes/sizes/create-size.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sizes"] = Size.objects.all()
        return context
