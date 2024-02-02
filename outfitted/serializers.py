"""
In Django REST framework, serializers act as translators between your complex Python 
models and the simpler data formats (like JSON) used by web APIs.
provides a mechanism for converting complex data types, such as Django models, into Python native data types
"""

from rest_framework import serializers
from .models import UserDetails, Product, Cart , Review
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

User = get_user_model()  # Retrieve the active user model


# ------------------------------------- REGISTRATION -------------------------------------------------
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'confirm_password', 'name', 'address', 'profile_pic', 'wishlist')  # Include all desired fields
        # exclude = ('last_login', 'is_superuser', 'first_name', 'last_name', 'is_staff')

    def save(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords must match.")

        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("Email already exists")

        attrs.pop('confirm_password')

        # Hash the password before creating the user
        attrs['password'] = make_password(attrs['password'])
        user = User.objects.create(**attrs)
            
        return user

# --------------------------------------------------------------------------------------
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(request=self.context.get('request'),
                            username=attrs.get('username'),
                            password=attrs.get('password'))
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        attrs['user'] = user
        return attrs
# ------------------------------------------------------------------------------------------
    

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
