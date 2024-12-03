from django_filters import FilterSet
from .models import *


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'product_name' : ['exact'],
            'product_price' : ['gt','lt'],
            'category_product' : ['exact']

        }