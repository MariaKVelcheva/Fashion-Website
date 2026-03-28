from django import forms

from fashionWebsite.clothes.models import Category, Color, Size, Garment


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


class BaseGarmentForm(forms.ModelForm):
    color = forms.ModelMultipleChoiceField(
        queryset=Color.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Garment
        exclude = ("slug", )
        labels = {
            "name": "Name",
            "category": "Category",
            "color": "Color",
            "size": "Size",
            "image": "Image",
            "description": "Description",
            "price": "Price",
            "stock": "Stock",
            "promotion": "Promotion",
        }
        widgets = {
            "category": forms.CheckboxSelectMultiple(),
            "size": forms.RadioSelect(),
            "description": forms.Textarea(attrs={"placeholder": "Description", "rows": 10}),
            "price": forms.NumberInput(),
            "stock": forms.NumberInput(),
            "promotion": forms.RadioSelect(),
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
        exclude = ("image", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].required = False
            self.fields[field].disabled = True

