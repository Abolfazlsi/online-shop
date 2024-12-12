from django import forms
from product.models import ContactUs

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ('email', 'text')

        widgets = {
            "email": forms.EmailInput(attrs={"class": "w-100 form-control border-0 py-3 mb-4", "placeholder": "ایمیل خود را وارد کنید"}),
            "text": forms.Textarea(attrs={"class": "w-100 form-control border-0 mb-4", "placeholder": "چیام خود را وارد کنید"}),
        }