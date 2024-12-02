from django.db import models
from account.models import User
from product.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    total = models.FloatField(default=0)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.phone

    class Meta:
        ordering = ("-created_at",)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderitems")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orderitems")
    quantity = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.product}"


class DiscountCode(models.Model):
    code = models.CharField(max_length=20)
    discount = models.SmallIntegerField(default=0)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.code


class UsedDiscountCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="UsedDiscountCodes")
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.CASCADE, related_name="UsedDiscountCodes")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="UsedDiscountCodes")

    def __str__(self):
        return self.user.phone