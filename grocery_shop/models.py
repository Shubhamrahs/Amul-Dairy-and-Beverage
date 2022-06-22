from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.expressions import F

User._meta.get_field("email")._unique = True
User._meta.get_field("email")._blank = False
User._meta.get_field("email")._null = False


class Owner(models.Model):
    name = models.CharField(max_length=200, null=False)
    email = models.CharField(max_length=200, null=False, primary_key = True)


class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=False)
    email = models.CharField(max_length=200, null=False)
    phone_number = models.CharField(max_length=10, null=False)


class Inventory(models.Model):
    CATEGORY = (
        ("Beverage", "Beverage"),
        ("Dairy_products", "Dairy_products"),
        ("Snacks", "Snacks"),
    )
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=200, null=False)
    product_image = models.ImageField(upload_to="images", null=True)
    category = models.CharField(max_length=200, choices=CATEGORY)
    required_quantity = models.IntegerField(null=True, default=1)
    quantity = models.IntegerField(null=False, default=1)
    price = models.FloatField(null=False)


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user_email = models.CharField(max_length=50)
    item = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=10)
