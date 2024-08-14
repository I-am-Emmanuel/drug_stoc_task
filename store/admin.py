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
    


# from django.contrib import admin, messages
# # from django.contrib.contenttypes.admin import GenericTabularInline
# from . import models
# # from tags.models import TaggedItem
# from django.db.models import Count, F
# from django.utils.html import format_html, urlencode
# from django.urls import reverse
# from django.db.models.query import QuerySet
# # from django.shortcuts import render
# # from django.http import HttpResponse

# # Register your models here.

# class InventoryFilter(admin.SimpleListFilter):
#     title = 'inventory'
#     parameter_name = 'inventory'

#     def lookups(self, request, model_admin):
#         return [
#             ('<10', 'Low')
#         ]
    
#     def queryset(self, request, queryset):
#         if self.value() == '<10':
#             return queryset.filter(inventory__lt=10)

   



# @admin.register(models.Product)
# class ProductAdmin(admin.ModelAdmin):
#     # fields = ['title', 'slug']
#     # exclude = []
#     # readonly_fields = []
   
#     autocomplete_fields = ['collection']
#     prepopulated_fields = {
#         'slug': ['title']
#     }
#     actions = ['clear_inventory']
#     # inlines = [TagInline]
#     list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
#     list_editable = ['unit_price']
#     list_per_page = 10
#     list_filter = ['collection', 'last_update', InventoryFilter]
#     list_select_related = ['collection']
#     search_fields = ['product']


#     def collection_title(self, product):
#         return product.collection.title

#     @admin.display(ordering='inventory')
#     def inventory_status(self, product):
#         if product.inventory < 10:
#             return 'Low'
#         return 'OK'

#     def clear_inventory(self, request, queryset):
#         updated_count = queryset.update(inventory=0)
#         self.message_user(
#             request,
#             f'{updated_count} products were succcessfully updated',
#             messages.ERROR

#         )


# class OrderItemInline(admin.StackedInline):
#     autocomplete_fields = ['product']
#     model = models.OrderItem
#     extra = 0
#     min_num = 1
#     max_num = 10

# @admin.register(models.Order)
# class OrderAdmin(admin.ModelAdmin):
#     autocomplete_fields = ['customer']
#     inlines = [OrderItemInline]
#     list_display = ['id', 'placed_at', 'customer']
#     # list_select_related = ['customer']
#     # ordering = ['first_name' 'last_name']
#     # def custumer_name(self, order):
#     #     return order.customer.first_name +' '+ order.customer.last_name

# # admin.site.register(models.Order)
           


# @admin.register(models.Collection)
# class CollectionAdmin(admin.ModelAdmin):
#     autocomplete_fields = ['featured_product']
#     list_display = ['title', 'products_count']
#     search_fields = ['title']

#     @admin.display(ordering='counted_products')
#     def products_count(self, collection):
#         # reverse('admin:app_model_page')
#         url = (
#             reverse('admin:store_product_changelist')
#              + '?' 
#              + urlencode({'collection__id': str(collection.id)}))
#         return format_html('<a href="{}">{}</a>',url, collection.products_count)
#         # return format_html('<a href="http://google.com>{}</a>', collection.counted_products)
#         # return collection.counted_products
    
#     def get_queryset(self, request):
#         return super().get_queryset(request).annotate(
#     products_count=Count('product')
#         )

# @admin.register(models.Customer)
# class CustomerAdmin(admin.ModelAdmin):
#     list_display = ['first_name', 'last_name', 'membership', 'customer_order']
#     list_editable = ['membership']
#     list_per_page = 10
#     ordering = ['user__first_name', 'user__last_name']
#     search_fields= ['first_name__istartswith', 'last_name__istartswith']
#     autocomplete_fields = ['user']
    
    

#     @admin.display(ordering='orders')
#     def customer_order(self, customer):
#         url = (reverse('admin:store_order_changelist') 
#         + '?'
#         + urlencode({'customer__id': str(customer.id)}))
#         return format_html('<a href="{}">{}</a>', url, customer.orders)

#     def get_queryset(self, request):
#         return super().get_queryset(request).annotate(orders=F('order'))
       
#         # return 
        