from django_filters.rest_framework import FilterSet
from .models import Product, Order
from django.utils import timezone
# from .permission import IsAdminOrReadOnly
# from rest_framework.decorators import action

# @action(detail=True, permission_classes= IsAdminOrReadOnly)
class ProductQuantityFilter(FilterSet):
    class Meta:
       model = Product
       fields = {
        'quantity': ['lt']
       } 

