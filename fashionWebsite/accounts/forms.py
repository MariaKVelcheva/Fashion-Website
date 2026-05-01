from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField, PasswordChangeForm, \
    AuthenticationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from fashionWebsite.accounts.models import Customer

AppUser = get_user_model()


class AppUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={"autofocus": True, "placeholder": _("Email")})
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": _("Password"),
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": _("Confirm Password"),
        })
    )

    error_messages = {
        "invalid_login": _("Invalid email or password."),
    }

    class Meta(UserCreationForm.Meta):
        model = AppUser
        fields = ("email", )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if AppUser.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Email already registered!"))
        return email

    def clean_password2(self):
        pw1 = self.cleaned_data.get("password1")
        pw2 = self.cleaned_data.get("password2")
        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError(_("Passwords don't match"))
        return pw2

    def clean(self):
        cleaned_data = super().clean()
        if self.errors:
            raise forms.ValidationError(_("Please correct the errors below."))
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AppUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = AppUser
        fields = "__all__"
        field_classes = {'email': UsernameField}


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': _('Email')})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": _("Password")}
        )
    )

    error_messages = {
        "invalid_login": _("Invalid email or password."),
    }

    def clean(self):
        cleaned_data = super().clean()
        if self.errors:
            raise forms.ValidationError(_("Invalid email or password."))
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].label = ""
        self.fields["username"].label = ""


class UpdateCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ("user", "favorites")
        widgets = {
            "telephone_number": forms.TextInput(attrs={"placeholder": _("Phone number")}),
            "address": forms.Textarea(attrs={"rows": 3})
        }
