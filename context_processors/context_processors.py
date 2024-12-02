from product.models import Product, Category
from cart.cart_module import Cart
from django.db.models import Avg
from django.db.models import Count


def best_products(request):
    best_product = Product.objects.all().order_by("-created_at")[:3]

    return {"best_product": best_product}


def products(request):
    all_product = Product.objects.all()[:9]

    return {"all_product": all_product}


def products_list(request):
    all_product = Product.objects.all()[:20]

    return {"products_list": all_product}


def cart_count(request):
    cart = Cart(request)

    return {"cart": cart}


def vegetable_category(request):
    vegetables_category = Category.objects.filter(name__icontains="vegetables").first()

    if vegetables_category:
        product_vegetables = Product.objects.filter(category=vegetables_category).order_by("-created_at")[:9]
    else:
        product_vegetables = Product.objects.none()

    return {"product_vegetables": product_vegetables}


def fruit_category(request):
    fruits_category = Category.objects.filter(name__icontains="fruits").first()

    if fruits_category:
        product_fruits = Product.objects.filter(category=fruits_category).order_by("-created_at")[:9]
    else:
        product_fruits = Product.objects.none()

    return {"product_fruits": product_fruits}


def bread_category(request):
    breads_category = Category.objects.filter(name__icontains="bread").first()

    if breads_category:
        product_breads = Product.objects.filter(category=breads_category).order_by("-created_at")[:9]
    else:
        product_breads = Product.objects.none()

    return {"product_breads": product_breads}


def meat_category(request):
    meats_category = Category.objects.filter(name__icontains="meat").first()

    if meats_category:
        product_meats = Product.objects.filter(category=meats_category).order_by("-created_at")[:9]
    else:
        product_meats = Product.objects.none()

    return {"product_meats": product_meats}


def product_popular(request):
    product = Product.objects.annotate(rating_count=Count("ratings")).order_by('-rating_count')[0]

    return {"popular": product}


def product_bestseller(request):
    product = Product.objects.annotate(rating_count=Count("ratings")).order_by('-rating_count')[0:7]

    return {"bestseller": product}


def categories(request):
    category = Category.objects.all()

    return {"categories": category}
