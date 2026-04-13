from django.urls import reverse_lazy
from django.views.generic import CreateView
from fashionWebsite.clothes.forms import CreateColorForm
from fashionWebsite.clothes.models import Color
from fashionWebsite.common.mixins import AdminRequiredMixin


class CreateColorView(AdminRequiredMixin, CreateView):
    model = Color
    form_class = CreateColorForm
    template_name = "clothes/colors/create-color.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["colors"] = Color.objects.all()
        return context