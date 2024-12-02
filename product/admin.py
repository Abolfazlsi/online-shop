from django.contrib import admin
from product.models import Category, Product, Rating, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    exclude = ("slug",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "min_weight")
    search_fields = ("name",)
    list_filter = ("price", "category")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("user", "product")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "product")
