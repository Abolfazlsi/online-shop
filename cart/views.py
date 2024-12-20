from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.generic import TemplateView, View, DetailView
from product.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from cart.cart_module import Cart
from cart.models import DiscountCode, Order, OrderItem, UsedDiscountCode
from django.conf import settings
import requests
import json
from account.models import Address
from django.http import JsonResponse, HttpResponseRedirect


class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, "cart/cart_detail.html", {"cart": cart})


class CartAddView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        quantity, color, size = request.POST.get("quantity"), request.POST.get("color", "empty"), request.POST.get(
            "size", "empty")
        cart = Cart(request)
        if quantity == "0" or int(quantity) < 0:
            return redirect("product:product_detail", product.slug)
        else:
            cart.add(product, quantity, color, size)
        return redirect("cart:cart_detail")


class CartDeleteView(View):
    def get(self, reqeust, id):
        cart = Cart(reqeust)
        cart.delete(id)
        return redirect("cart:cart_detail")


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "cart/order_detail.html"


class OrderCreationView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user, total=cart.final_total())
        for item in cart:
            OrderItem.objects.create(order=order, product=item["product"], quantity=item["quantity"], size=item["size"],
                                     color=item["color"], price=item["price"])
        cart.remove_cart()

        return redirect("cart:order_detail", order.id)


class DiscountView(View):
    def post(self, request, pk):
        code = request.POST.get('discount')
        order = get_object_or_404(Order, id=pk)
        discount_code = get_object_or_404(DiscountCode, code=code)
        if UsedDiscountCode.objects.filter(user=request.user, discount_code=discount_code, order=order).exists():
            return redirect("cart:order_detail", order.id)
        if discount_code.quantity == 0:
            discount_code.delete()
            return redirect("cart:order_detail", order.id)
        order.total -= order.total * discount_code.discount / 100
        order.save()
        UsedDiscountCode.objects.create(user=request.user, discount_code=discount_code, order=order)
        discount_code.quantity -= 1
        discount_code.save()

        return redirect("cart:order_detail", order.id)


if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'payment'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/v4/payment/request.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/v4/payment/verify.json"

description = "نهایی کردن خرید شما از سایت ما"

CallbackURL = 'http://127.0.0.1:8000/cart/verify/'


class SendRequestView(View):
    def post(self, request, pk):
        # بازیابی سفارش بر اساس شناسه و کاربر
        order = get_object_or_404(Order, id=pk, user=request.user)

        # بازیابی آدرس از POST
        address = get_object_or_404(Address, id=request.POST.get("address"))

        # تنظیم آدرس سفارش
        order.full_name = f"{address.fullname}"
        order.address = f"{address.address}"
        order.phone_number = f"{address.phone}"
        order.postal_code = f"{address.postal_code}"
        order.save()

        # ذخیره شناسه سفارش در جلسه
        request.session["order_id"] = str(order.id)

        # آماده‌سازی داده‌ها برای ارسال به API
        data = {
            "merchant_id": settings.MERCHANT,
            "amount": order.total,
            "description": description,
            "callback_url": CallbackURL,
        }
        data = json.dumps(data)

        # تنظیم هدرها
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}

        # ارسال درخواست به API
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers)

        # بررسی پاسخ API
        if response.status_code == 200:
            response = response.json()

            if response["data"]['code'] == 100:
                url = f"{ZP_API_STARTPAY}{response['data']['authority']}"
                return redirect(url)
            else:
                return HttpResponse(str(response['errors']))
        else:
            return render(request, "cart/Buy_Error.html", {})



class VerifyView(View):
    def get(self, request):
        status = request.GET.get('Status')
        authority = request.GET.get('Authority')
        order = Order.objects.get(id=int(request.session['order_id']))

        if status == "OK":


            data = {
                "merchant_id": settings.MERCHANT,
                "amount": order.total,
                "authority": authority
            }
            data = json.dumps(data)

            headers = {'content-type': 'application/json', 'Accept': 'application/json'}

            response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

            if response.status_code == 200:
                response = response.json()
                if response['data']['code'] == 100:
                    order.is_paid = True
                    order.save()
                    return render(request, "cart/successfully_pay.html", {"order": order})
                elif response['data']['code'] == 101:
                    return render(request, "cart/pay_again.html", {})
                else:
                    return render(request, "cart/unsuccessful_pay.html", {})
            else:
                return render(request, "cart/unsuccessful_pay.html", {})
        else:
            return render(request, "cart/unsuccessful_pay.html", {})