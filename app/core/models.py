from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

from django.db.models.signals import post_save
from django.dispatch import receiver


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email,
            name,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=150, unique=True, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    categories = models.ManyToManyField(Category, blank=True, related_name='products')
    # image = models.ImageField(upload_to=product_image)


@receiver(post_save, sender=Product)
def update_is_available(sender, instance, **kwargs):
    if instance.quantity > 0:
        Product.objects.filter(pk=instance.pk).update(is_available=True)
    else:
        Product.objects.filter(pk=instance.pk).update(is_available=False)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items', null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items', null=True)
    quantity = models.PositiveIntegerField(default=1)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    DELIVERY_STATUS = (
        ('Waiting for payment', 'Waiting for payment'),
        ('Collecting order', 'Collecting order'),
        ('Sent', 'Sent'),
    )
    delivery_status = models.CharField(max_length=100, choices=DELIVERY_STATUS, default='Waiting for payment')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=0)



