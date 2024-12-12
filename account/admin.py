from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from account.forms import UserCreationForm, UserChangeForm
from account.models import User, Otp, Address, MyInfo


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ["phone", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["phone", "password"]}),
        (None, {"fields": ["fullname"]}),
        (None, {"fields": ["email"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["phone", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["phone"]
    ordering = ["phone"]
    filter_horizontal = []


@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ("phone", "code")


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "fullname", "email", "postal_code")


@admin.register(MyInfo)
class MyInfoAdmin(admin.ModelAdmin):
    list_display = ("address", "email")


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
