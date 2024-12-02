from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View, DetailView
from product.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from cart.cart_module import Cart
from cart.models import DiscountCode, Order, OrderItem, UsedDiscountCode


class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, "cart/cart_detail.html", {"cart": cart})


class CartAddView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        quantity = request.POST.get("quantity")
        cart = Cart(request)
        if quantity == "0" or int(quantity) < 0:
            return redirect("product:product_detail", product.slug)
        else:
            cart.add(product, quantity)
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
            OrderItem.objects.create(order=order, product=item["product"], quantity=item["quantity"],
                                     price=item["price"])
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
