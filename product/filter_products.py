from django.core.paginator import Paginator


def products_filter(request, queryset):
    # دریافت پارامترهای فیلتر از درخواست
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    filter_type = request.GET.get("filter")
    colors = request.GET.getlist("color")
    sizes = request.GET.getlist("size")
    page_number = request.GET.get("page", 1)

    # اعمال فیلتر قیمت
    if min_price and max_price:
        queryset = queryset.filter(price__gte=min_price, price__lte=max_price).distinct()

    # اعمال مرتب‌سازی
    if filter_type == "cheapest":
        queryset = queryset.order_by("price")
    elif filter_type == "expensive":
        queryset = queryset.order_by("-price")

    # اعمال فیلتر رنگ
    if colors:
        queryset = queryset.filter(color__name__in=colors).distinct()

    # اعمال فیلتر سایز
    if sizes:
        queryset = queryset.filter(size__name__in=sizes).distinct()

    # صفحه‌بندی
    paginator = Paginator(queryset, 9)
    objects_list = paginator.get_page(page_number)

    # آماده‌سازی context
    context = {
        "product_list": objects_list,
        "selected_colors": colors,
        "selected_sizes": sizes
    }

    return context
