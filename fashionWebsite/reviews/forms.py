from django import forms

from fashionWebsite.reviews.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("rating", "text",)

        labels = {
            "rating": "Rating",
            "text": "Review",
        }

        widgets = {
            "rating": forms.Select(),
            "text": forms.Textarea(attrs={"placeholder": "Write your review...", }),
        }

    def clean_text(self):
        text = self.cleaned_data.get("text", "")
        if text and not text.strip():
            raise forms.ValidationError("Please, write a review.")
        return text.strip()


class UpdateReviewForm(ReviewForm):
    pass
