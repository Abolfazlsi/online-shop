from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from account.models import User, Address
from django.core.exceptions import ValidationError
from django.core import validators


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["phone"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["phone", "fullname", "password", "is_active", "is_admin"]


class OtpRegisterLoginForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(
        attrs={"class": "w-100 form-control border-0 py-3 mb-4", "placeholder": "Enter your phone"}),
        validators=[validators.MaxLengthValidator(11)])


class OtpVerifyForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(
        attrs={"class": "w-100 form-control border-0 py-3 mb-4", "placeholder": "Enter yore code ..."}),
        validators=[validators.MaxLengthValidator(4)])


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["fullname", "email", ]

        widgets = {
            "fullname": forms.TextInput(attrs={"class": "w-100 form-control border-0 py-3 mb-4"}),
            "email": forms.TextInput(attrs={"class": "w-100 form-control border-0 py-3 mb-4"}),
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ("fullname", "phone", "address", "email", "postal_code")
        widgets = {
            "fullname": forms.TextInput(attrs={"class": "w-100 form-control border-0 py-3 mb-4"}),
            "phone": forms.TextInput(attrs={"class": "w-100 form-control border-0 py-3 mb-4"}),
            "address": forms.Textarea(attrs={"class": "w-100 form-control border-0 py-3 mb-4"}),
            "email": forms.EmailInput(attrs={"class": "w-100 form-control border-0 py-3 mb-4"}),
            "postal_code": forms.TextInput(attrs={"class": "w-100 form-control border-0 py-3 mb-4"})
        }
