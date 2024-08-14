from django.db import models
from django.contrib import admin
from django.conf import settings
from  django.core.validators import MinValueValidator
from uuid import uuid4


# Create your models here.


class Customer(models.Model):
    '''customer table'''
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    

    def __str__(self) -> str:
            return f'{self.user.first_name} {self.user.last_name}'
    
    @admin.display(ordering='user__first_name')
    def first_name(self) -> str:
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self) -> str:
        return self.user.last_name

    class Meta:
        ordering = ['user__first_name', 'user__last_name']

class Product(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=False, null=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(1)])
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = ['title']
  
class Order(models.Model):
    PENDING_ORDER = 'P'
    CANCELLED_ORDER = 'X'
    COMPLETED_ORDER = 'C'

    ORDER_STATUS_CHOICES = [
    (PENDING_ORDER, 'Pending'),
    (CANCELLED_ORDER, 'Cancelled'),
    (COMPLETED_ORDER, 'Completed'),

]
    placed_at = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=1, choices=ORDER_STATUS_CHOICES, default=PENDING_ORDER)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    
    def __str__(self) -> str:
        return f'{self.placed_at}'
    
    class Meta:
        '''custom permission for cancelling an order instead of deleting it. 
        This give some admin user permission to cancel an order but not update it'''
        
        permissions = [
            ('cancel_order', 'Can cancel order')
        ]


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = [['cart', 'product']]