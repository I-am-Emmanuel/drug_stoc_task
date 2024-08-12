from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.


class Customer(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['first_name', 'last_name']

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
    CANCELLED_ORDER = 'CA'
    COMPLETED_ORDER = 'C'

    ORDER_STATUS_CHOICES = [
    (PENDING_ORDER, 'Pending'),
    (CANCELLED_ORDER, 'Cancelled'),
    (COMPLETED_ORDER, 'Completed'),

]
    placed_at = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=2, choices=ORDER_STATUS_CHOICES, default=PENDING_ORDER)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    
    

    class Meta:
        ordering = ['placed_at']


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_details')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
