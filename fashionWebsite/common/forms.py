from django import forms
from django.utils.translation import gettext_lazy as _
from fashionWebsite.common.models import NewsletterSubscriber


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label=_('Name'),
    )

    email = forms.EmailField(
        label=_("Email"),
    )

    message = forms.CharField(
        label=_("Your message"),
        widget=forms.Textarea(),
    )


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ("email",)
        widgets = {
            "email": forms.EmailInput(attrs={
                "placeholder": _("Enter your email address"),
            })
        }

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if NewsletterSubscriber.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError(_("This email is already subscribed."))
        return email
