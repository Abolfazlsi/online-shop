from product.models import Product, Category
from cart.cart_module import Cart
from django.db.models import Avg
from django.db.models import Count
from account.models import MyInfo


def products(request):
    all_product = Product.objects.all()[:8]

    return {"all_product": all_product}


def products_list(request):
    all_product = Product.objects.all()[:20]

    return {"products_list": all_product}


def cart_count(request):
    cart = Cart(request)

    return {"cart": cart}


def phone_category(request):
    phones_category = Category.objects.filter(name__icontains="Phone").first()

    if phones_category:
        product_phone = Product.objects.filter(category=phones_category).order_by("-created_at")[:9]
    else:
        product_phone = Product.objects.none()

    return {"product_phone": product_phone}


def pc_category(request):
    pcc_category = Category.objects.filter(name__icontains="PC").first()

    if pcc_category:
        product_pc = Product.objects.filter(category=pcc_category).order_by("-created_at")[:9]
    else:
        product_pc = Product.objects.none()

    return {"product_pc": product_pc}


def laptop_category(request):
    laptops_category = Category.objects.filter(name__icontains="Laptop").first()

    if laptops_category:
        product_laptops = Product.objects.filter(category=laptops_category).order_by("-created_at")[:9]
    else:
        product_laptops = Product.objects.none()

    return {"product_laptops": product_laptops}


def charger_category(request):
    chargers_category = Category.objects.filter(name__icontains="Charger").first()

    if chargers_category:
        product_chargers = Product.objects.filter(category=chargers_category).order_by("-created_at")[:9]
    else:
        product_chargers = Product.objects.none()

    return {"product_chargers": product_chargers}


def product_popular(request):
    product = Product.objects.annotate(rating_count=Count("ratings")).order_by('-rating_count')[0]

    return {"popular": product}


def product_bestseller(request):
    product = Product.objects.annotate(rating_count=Count("ratings")).order_by('-rating_count')[0:7]

    return {"bestseller": product}


def categories(request):
    category = Category.objects.all()

    return {"categories": category}


def related_product(request):
    related_products = Product.objects.filter()


def my_info(request):
    info = MyInfo.objects.all().last()

    return {"info": info}
