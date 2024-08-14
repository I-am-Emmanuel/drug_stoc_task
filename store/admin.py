from django.contrib import admin
from store.models import Customer, Product, Order, OrderDetail


# Register your models here.
# admin.site.register(Customer)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']
    list_per_page = 10
    list_select_related = ['user']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    ordering = ['user__first_name', 'user__last_name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'price', 'quantity']
    list_editable = ['price', 'quantity']
    list_per_page = 10
    search_fields = ['title__istartswith']
    list_filter = ['quantity', 'price']
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['placed_at', 'order_status']
    list_per_page = 10
    search_fields = ['customer__first_name__istartswith']
    list_filter = ['placed_at']

    def collection_name(self, customer):
        return customer.first_name
    
    
@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity']
    list_per_page = 10
    