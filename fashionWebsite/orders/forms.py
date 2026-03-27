from django import forms

from fashionWebsite.orders.models import Promotion


class PromotionBaseForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = '__all__'
        labels = {
            "code": "Code",
            "type": "Type",
            "discount_percent": "Discount %",
            "valid_from": "Valid from",
            "valid_until": "Valid until",
            "categories": "Categories",
        }

        widgets = {
            "code": forms.TextInput(
                attrs={"placeholder": "Promotional code..."}),
            "type": forms.RadioSelect(),
            "valid_from": forms.DateInput(
                attrs={"type": "date", },
            ),
            "valid_until": forms.DateInput(
                attrs={"type": "date", },
            ),
            "discount_percent": forms.NumberInput(
                attrs={"min": "0", "max": "100", "step": "0.1"}
            ),
            "categories": forms.CheckboxSelectMultiple(),
        }

    def clean(self):
        cleaned_data = super().clean()
        valid_from = cleaned_data.get("valid_from")
        valid_until = cleaned_data.get("valid_until")

        if valid_from and valid_until and valid_from >= valid_until:
            raise forms.ValidationError("The starting date should come before the end date.")

        return cleaned_data


class CreatePromotionForm(PromotionBaseForm):
    pass


class UpdatePromotionForm(PromotionBaseForm):
    pass
