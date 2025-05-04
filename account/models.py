from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        if not phone:
            raise ValueError("Users must have an phone")

        user = self.model(
            phone=phone
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        null=True,
        blank=True,
        unique=True
    )
    fullname = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=11, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "phone"

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Otp(models.Model):
    token = models.CharField(max_length=11, null=True)
    phone = models.CharField(max_length=11)
    code = models.SmallIntegerField()
    expire = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    fullname = models.CharField(max_length=200)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=11)
    postal_code = models.CharField(max_length=11)

    def __str__(self):
        return f"{self.user.phone}"

class MyInfo(models.Model):
    address = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.address} - {self.email}"
