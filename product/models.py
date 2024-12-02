from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from account.models import User
from django.db.models import Avg

<<<<<<< HEAD
=======

>>>>>>> add-option-to-product
class Category(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, null=True, blank=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def save(self, *args, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name, allow_unicode=True)
        super(Category, self).save()


<<<<<<< HEAD
=======
class Color(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


>>>>>>> add-option-to-product
class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField(default=0)
    product_image = models.ImageField(upload_to="product_images")
    category = models.ManyToManyField("product.Category", related_name="products")
<<<<<<< HEAD
    min_weight = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    quality = models.CharField(max_length=50)
=======
    color = models.ManyToManyField("product.Color", related_name="products")
    size = models.ManyToManyField("product.Size", related_name="products", null=True, blank=True)
>>>>>>> add-option-to-product
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, null=True, blank=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def save(self, *args, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name, allow_unicode=True)
        super(Product, self).save()

    def get_absolute_url(self):
        return reverse("product:product_detail", args=[self.slug])

    class Meta:
        ordering = ("-created_at",)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="ratings")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.product}"

    class Meta:
        ordering = ("-created_at",)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.text}"

    def time_since_creation(self):
        time_delta = timezone.now() - self.created_at
        days = time_delta.days
        hours, remainder = divmod(time_delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if days >= 365:
            years = days // 365
            return f"{years} years ago"
        elif days >= 30:
            months = days // 30
            return f"{months} months ago"
        elif days > 0:
            return f"{days} days ago"
        elif hours > 0:
            return f"{hours} hours ago"
        elif minutes > 0:
            return f"{minutes} minutes ago"
        else:
            return f"{seconds} seconds ago"

    class Meta:
        ordering = ("-created_at",)
