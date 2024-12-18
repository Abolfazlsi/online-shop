from django.urls import path
from cart import views

app_name = "cart"
urlpatterns = [
    path("cart-detail/", views.CartDetailView.as_view(), name="cart_detail"),
    path("cart-add/<int:pk>/", views.CartAddView.as_view(), name="cart_add"),
    path("cart-delte/<str:id>/", views.CartDeleteView.as_view(), name="cart_delete"),
    path("order-detail/<int:pk>/", views.OrderDetailView.as_view(), name="order_detail"),
    path("order-creation/", views.OrderCreationView.as_view(), name="order_creation"),
    path("discount-code/<int:pk>", views.DiscountView.as_view(), name="discount_code"),
    path("send-request/<int:pk>", views.SendRequestView.as_view(), name="send_request"),
    path("verify/", views.VerifyView.as_view(), name="verify_request"),
]
