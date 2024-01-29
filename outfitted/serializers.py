"""
In Django REST framework, serializers act as translators between your complex Python 
models and the simpler data formats (like JSON) used by web APIs.
provides a mechanism for converting complex data types, such as Django models, into Python native data types
"""

from rest_framework import serializers
from .models import UserDetails, Product, Cart , Review

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['id', 'name', 'address', 'email', 'profile_pic', 'wishlist']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['productid', 'category', 'Images', 'name', 'description', 'price', 'ratings', 'buys', 'mrp', 'discount', 'title', 'size', 'product_code', 'color', 'seller']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['user', 'product', 'quantity']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['user', 'product', 'review']
