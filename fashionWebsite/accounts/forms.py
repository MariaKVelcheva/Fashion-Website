from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField, PasswordChangeForm, \
    AuthenticationForm
from django.contrib.auth import get_user_model

from fashionWebsite.accounts.models import Customer

AppUser = get_user_model()


class AppUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = AppUser
        fields = ("email", )
        field_classes = {"email": UsernameField}

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if AppUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered!")
        return email


class AppUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = AppUser
        fields = "__all__"
        field_classes = {'email': UsernameField}


class LoginForm(AuthenticationForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].label = ""
        self.fields["email"].label = ""


class UpdateCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ("user", )
        widgets = {
            "telephone_number": forms.TextInput(attrs={"placeholder": "Phone"}),
            "address": forms.Textarea(attrs={"rows": 3})
        }
