from django.urls import path, re_path
from product import views

app_name = "product"
urlpatterns = [
    re_path(r"product-detail/(?P<slug>[-\w]*)/", views.ProductDetailView.as_view(), name="product_detail"),
    re_path(r"rating/(?P<slug>[-\w]*)/", views.RatingsView.as_view(), name="rating"),
    path("products-list/", views.ProductsListView.as_view(), name="products_list"),
    path("search-product/", views.SearchProductView.as_view(), name="search_product"),
    re_path(r"category-detail/(?P<slug>[-\w]*)/", views.CategoryDetailView.as_view(), name="category_detail"),
    path("contact-us/", views.ContactUsView.as_view(), name="contact_us"),
]
