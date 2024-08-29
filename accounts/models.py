from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(email, name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin


class Product(models.Model):
    brand_name = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    product_image = models.URLField(max_length=2000)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    deal_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    sizes = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    category = models.CharField(max_length=255)

    class Meta:
        unique_together = ('brand_name', 'product_name', 'offer_price')

    def __str__(self):
        return self.product_name
