from django import forms

from fashionWebsite.clothes.models import Category, Color, Size, Garment
from fashionWebsite.orders.models import Promotion

from django.forms import inlineformset_factory
from .models import Product


class BaseCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name", "profile_image")
        labels = {
            "name": "Name",
        }
        widgets = {
            "name": forms.TextInput(attrs={'placeholder': 'Category name'})
        }


class BaseColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = "__all__"
        labels = {
            "name": "Name",
            "hex_code": "Hex Code",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Color name"}),
            "hex_code": forms.TextInput(attrs={'placeholder': 'Hex Code...'}),
        }


class BaseSizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = ("name", )
        labels = {
            "name": "Name",
        }
        widgets = {"name": forms.TextInput(attrs={"placeholder": "Size type"}),}


ProductFormSet = inlineformset_factory(
    Garment,
    Product,
    fields=("size", "color", "stock"),
    extra=1,
    can_delete=True
)


class BaseGarmentForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Garment
        exclude = ("slug", )
        labels = {
            "name": "Name",
            "category": "Category",
            "profile_image": "Image",
            "description": "Description",
            "price": "Price",
            "main_image": "Main image",
        }
        widgets = {
            "description": forms.Textarea(attrs={"placeholder": "Description", "rows": 5, "cols": 10}),
            "price": forms.NumberInput(attrs={'placeholder': 'Price (€)'}),
            "name": forms.TextInput(attrs={'placeholder': 'Name'}),
        }


class CreateCategoryForm(BaseCategoryForm):
    pass


class UpdateCategoryForm(BaseCategoryForm):
    pass


class CreateColorForm(BaseColorForm):
    pass


class CreateSizeForm(BaseSizeForm):
    pass


class CreateGarmentForm(BaseGarmentForm):
    pass


class UpdateGarmentForm(BaseGarmentForm):
    pass


class DeleteGarmentForm(BaseGarmentForm):
    class Meta(BaseGarmentForm.Meta):
        exclude = ("main_image", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].required = False
            self.fields[field].disabled = True

