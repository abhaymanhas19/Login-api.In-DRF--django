from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

# from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import SeteraUser, UserRoles

# # Register your models here.


class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = SeteraUser
    search_fields = ("email",)
    list_display = (
        "id",
        "first_name",
        "email",
        "last_name",
        "mobile",
        "organization",
        "is_staff",
        "is_active",
        "date_joined",
        "role",
    )
    list_filter = (
        "role",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "mobile",
                    "email",
                    "password",
                    "organization",
                    "role",
                    "date_joined",
                    "last_login",
                )
            },
        ),
        ("Permissions", {"fields": ("is_superuser", "is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "mobile",
                    "password1",
                    "password2",
                    "organization",
                    "role",
                ),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_superuser",
                    "is_staff",
                    "is_active",
                )
            },
        ),
    )
    search_fields = (
        "first_name",
        "email",
        "organization__name",
    )
    ordering = ("email",)


admin.site.register(SeteraUser, CustomUserAdmin)


@admin.register(UserRoles)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = [
        "name",
    ]
