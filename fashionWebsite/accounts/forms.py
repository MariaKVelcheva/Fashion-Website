from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField, PasswordChangeForm
from django.contrib.auth import get_user_model


AppUser = get_user_model()


class AppUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = AppUser
        fields = ("email", )
        field_classes = {'email': UsernameField}


class AppUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = AppUser
        fields = "__all__"
        field_classes = {'email': UsernameField}

