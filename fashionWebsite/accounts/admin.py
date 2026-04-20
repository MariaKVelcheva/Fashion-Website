from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from fashionWebsite.accounts.forms import AppUserChangeForm, AppUserCreationForm
from fashionWebsite.accounts.models import Customer

AppUser = get_user_model()


class CustomerInline(admin.StackedInline):
    model = Customer
    can_delete = False
    verbose_name_plural = 'Profiles'
    fk_name = 'user'


@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    inlines = [CustomerInline]
    fieldsets = (
        (None, {"fields": ("email", "password",)}),
        (_("Personal info"), {"fields": ("loyalty_points", )}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", )}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    form = AppUserChangeForm
    add_form = AppUserCreationForm
    change_password_form = None
    list_display = ("email", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

