from django import forms

from fashionWebsite.clothes.models import Category, Color, Size, Garment


class CategoryBaseForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name", )
        labels = {
            "name": "Name",
        }
        widgets = {
            "name": forms.RadioSelect()
        }


class ColorBaseForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = "__all__"
        labels = {
            "name": "Name",
            "hex_code": "Hex Code",
        }
        widgets = {
            "name": forms.RadioSelect(),
            "hex_code": forms.TextInput(attrs={'placeholder': 'Hex Code...'}),
        }


class SizeBaseForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = ("name", )
        labels = {
            "name": "Name",
        }
        widgets = {"name": forms.RadioSelect()}


class GarmentBaseForm(forms.ModelForm):
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
            "color": forms.CheckboxSelectMultiple(),
            "size": forms.RadioSelect(),
            "description": forms.TextInput(attrs={'placeholder': 'Description'}),
            "price": forms.NumberInput(),
            "stock": forms.NumberInput(),
            "promotion": forms.RadioSelect(),
            "name": forms.TextInput(attrs={'placeholder': 'Name'}),
        }


class CategoryCreateForm(CategoryBaseForm):
    pass


class CategoryEditForm(CategoryBaseForm):
    pass


class CategoryDeleteForm(CategoryBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.required = False
            field.disabled = True


class ColorCreateForm(ColorBaseForm):
    pass


class ColorDeleteForm(ColorBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.required = False
            self.fields[field].disabled = True


class SizeCreateForm(SizeBaseForm):
    pass


class SizeDeleteForm(SizeBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.required = False
            self.fields[field].disabled = True


class GarmentCreateForm(GarmentBaseForm):
    pass


class GarmentEditForm(GarmentBaseForm):
    pass


class GarmentDeleteForm(GarmentBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].required = False
            self.fields[field].disabled = True

