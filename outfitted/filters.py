# filters.py
import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category', lookup_expr='iexact')
    name = django_filters.CharFilter(field_name='name', lookup_expr='iexact')
    price = django_filters.BaseRangeFilter(field_name='price')
    discount = django_filters.NumberFilter(field_name='discount', lookup_expr='gte')
    ratings = django_filters.NumberFilter(field_name='ratings', lookup_expr='gte')
    seller = django_filters.CharFilter(field_name='seller', lookup_expr='iexact')

    class Meta:
        model = Product
        fields = ['category', 'name', 'price', 'ratings', 'discount', 'seller']
