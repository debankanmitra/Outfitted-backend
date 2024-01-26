"""
This file is used to define the data models for your application. 
Each model corresponds to a database table and defines the fields and behaviors of the table.
"""


from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid


# Create your models here.


class UserDetails(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255,blank=True)
    profile_pic = models.CharField(max_length=255,blank=True)
    wishlist = ArrayField(models.CharField(max_length=255),default=list)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    productid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )
    category = models.CharField(max_length=255)
    Images = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    ratings = models.IntegerField(max_length=255)
    buys = models.IntegerField(max_length=255)
    mrp = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.IntegerField(max_length=255)

    title = models.CharField(max_length=255,  blank=True)
    size = models.CharField(max_length=255,  blank=True)
    product_code = models.CharField(max_length=255,  blank=True)
    color = models.CharField(max_length=255,  blank=True)
    seller = models.CharField( blank=True)

    def __str__(self):
        return self.name

    
class Cart(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product


# The on_delete=models.CASCADE option means that when a referenced ProductCard is deleted, 
    # also delete the ProductDetails instances associated with it.
class Review(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.CharField(max_length=255)
    rating = models.IntegerField(max_length=255)
    date = models.DateField()
    likes = models.IntegerField()
    dislikes = models.IntegerField()

    def __str__(self):
        return self.product

