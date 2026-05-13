from django import forms
from django.utils.translation import gettext_lazy as _
from fashionWebsite.reviews.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("rating", "text",)

        labels = {
            "rating": _("Rating"),
            "text": _("Review"),
        }

        widgets = {
            "rating": forms.Select(),
            "text": forms.Textarea(attrs={"placeholder": _("Write your review..."), }),
        }

    def clean_text(self):
        text = self.cleaned_data.get("text", "")
        if text and not text.strip():
            raise forms.ValidationError(_("Please, write a review."))
        return text.strip()


class UpdateReviewForm(ReviewForm):
    pass
