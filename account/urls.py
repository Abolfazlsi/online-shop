from django.urls import path
from account import views

app_name = "account"
urlpatterns = [
    path("register-login/", views.RegisterView.as_view(), name="register_login"),
    path("otp_verify/", views.OtpVerifyView.as_view(), name="otp"),
    path("user-profile/", views.UserProfileView.as_view(), name="user_profile"),
    path("add-address/", views.AddressView.as_view(), name="add_address"),
]
