"""
This file is used to define the data models for your application. 
Each model corresponds to a database table and defines the fields and behaviors of the table.
"""


from email.policy import default
from enum import unique
from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid
from django.contrib.auth.models import AbstractUser



# Create your models here.

class User(AbstractUser):
    id = models.UUIDField( primary_key=True, default=uuid.uuid4, editable=False, unique=True, auto_created=True)
    name = models.CharField(max_length=255,blank=True)
    address = models.TextField(max_length=255,blank=True)
    email = models.EmailField(max_length=255,unique=True)
    profile_pic = models.ImageField(max_length=255,null=True,blank=True, upload_to='profile_pics')
    wishlist = ArrayField(models.CharField(max_length=255),default=list,null=True,blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username
    

class Product(models.Model):
    
    productid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False, auto_created=True,
    )
    category = models.CharField(max_length=255)
    Images = models.CharField(max_length=255, unique=True, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    ratings = models.FloatField()
    buys = models.IntegerField()
    mrp = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.FloatField()

    title = models.TextField(max_length=255,  blank=True)
    size = models.CharField(max_length=255,  blank=True) # for choice: https://docs.djangoproject.com/en/5.0/topics/db/models/
    product_code = models.CharField(max_length=255,  blank=True)
    color = models.CharField(max_length=255,  blank=True)
    seller = models.CharField(blank=True)
        
    def __str__(self):
        return self.name

    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product


# The on_delete=models.CASCADE option means that when a referenced ProductCard is deleted, 
    # also delete the ProductDetails instances associated with it.
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField(max_length=255)
    rating = models.IntegerField()
    date = models.DateField()
    likes = models.IntegerField()
    dislikes = models.IntegerField()

    def __str__(self):
        return self.product


# extras ------------------------------------------------------------------
# pass statement is a null operation, and it will not affect the interpretation of the class's fields.

class Order(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False, auto_created=True,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=255)


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class Payment(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False, auto_created=True,
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    method = models.CharField(max_length=255)
