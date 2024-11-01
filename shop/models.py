from django.db import models
from user.models import User
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=225)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=225)
    description = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='product_images/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.DecimalField(max_digits=15, decimal_places=2)
    STATUS_CHOICES = [
        ("Awaiting", "Awaiting payment"),
        ("Paid", "Paid"),
        ("Sending", "Sending")
    ]
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    order_date = models.DateField(auto_now_add=True)
    shipping_address = models.TextField()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=15, decimal_places=2)


