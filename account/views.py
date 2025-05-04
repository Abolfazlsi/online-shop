from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, CreateView
from account.forms import OtpRegisterLoginForm, OtpVerifyForm, UserProfileForm, AddressForm
import random
from account.models import Otp, User, Address
from uuid import uuid4
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from account.tasks import delete_otp


# register user
class RegisterView(View):
    # if request was get just show form
    def get(self, request):
        form = OtpRegisterLoginForm()
        return render(request, "account/register.html", {"form": form})

    def post(self, request):
        # if request was post get data
        form = OtpRegisterLoginForm(request.POST)
        if form.is_valid():
            code = random.randint(1000, 9999)
            phone = form.cleaned_data["phone"]
            token = str(uuid4())
            otp = Otp.objects.create(token=token, phone=phone, code=code)
            delete_otp.apply_async(args=[otp.id], countdown=120)
            print(code)  # for test

            return redirect(reverse("account:otp") + f"?token={token}")
        else:
            form.add_error("phone", "invalid data")

        return render(request, "account/register.html", {"form": form})


class OtpVerifyView(View):
    # if request was get just show form
    def get(self, request):
        form = OtpVerifyForm()
        return render(request, "account/otp_verify.html", {"form": form})

    def post(self, request):
        token = request.GET.get("token")
        form = OtpVerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            if Otp.objects.filter(code=code, token=token).exists():
                otp = Otp.objects.get(token=token)
                user, create = User.objects.get_or_create(phone=otp.phone)
                login(request, user, backend="django.contrib.auth.backends.ModelBackend")
                otp.delete()
                return redirect("home:home")
            else:
                form.add_error("code", "invalid data")
        else:
            form.add_error("code", "invalid data")
        return render(request, "account/otp_verify.html", {"form": form})


class LogOutView(View):
    def get(self, request):

        if request.user.is_authenticated:
            logout(request)
            return redirect("home:home")
        else:
            return redirect("home:home")


class UserProfileView(View):
    def get(self, request):
        user = request.user
        form = UserProfileForm(instance=user)
        return render(request, "account/user_profile.html", {"form": form})

    def post(self, request):
        user = request.user
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("account:user_profile")
        return render(request, "account/user_profile.html", {"form": form})


class AddressView(CreateView):
    model = Address
    form_class = AddressForm
    template_name = "account/address.html"
    success_url = reverse_lazy("account:add_address")

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        next_page = self.request.GET.get("next")
        if next_page:
            return redirect(next_page)
        return super().form_valid(form)
