from .models import Customer, Product, Order, OrderDetail,Order, Cart, CartItem
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'price', 'quantity', 'description']



class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item:CartItem):
        '''calculate price of each item and its quantity'''
        return cart_item.quantity * cart_item.product.price
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']
    
class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart:Cart):
        '''calculate price of all items in a cart'''
        return sum([item.quantity * item.product.price for item in cart.items.all()])
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price'] 

class AddCartItemSerializer(serializers.ModelSerializer):
    '''Add and save item inside the cart if but check if
        the item exist. If item exists, the item quantity 
        will only be added to the existing quantity, otherwise a new item 
        and its quantity will be created and save in the cart. 
    '''
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        '''check if the product exist before adding to the cart. If exist, then the 
        product id will be added, but if otherwise it raise a validation error'''
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No Product with the given ID was found.')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
            # Update an existing item 
        except CartItem.DoesNotExist:
            # Create a new item 
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']



class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields= ['id', 'user_id', 'phone', 'birth_date']

class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderDetail
        fields = ['id', 'product', 'unit_price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'order_status', 'items']

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No cart with the given ID was found')
        if CartItem.objects.filter(cart_id= cart_id).count() == 0:
            raise serializers.ValidationError('The cart is empty.')
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():

            cart_id = self.validated_data['cart_id']
            # print(self.validated_data['cart_id'])
            # print(self.context['user_id'])

            customer= Customer.objects.get(user_id=self.context['user_id'])
            order = Order.objects.create(customer=customer)

            cart_items = CartItem.objects\
                        .select_related('product')\
                        .filter(cart_id=cart_id)
            order_items = [
                OrderDetail(
                    order= order, 
                    product=item.product, 
                    unit_price=item.product.unit_price, 
                    quantity=item.quantity
                ) for item in cart_items
            ]
            OrderDetail.objects.bulk_create(order_items)
            
            Cart.objects.filter(pk=cart_id).delete()

            order_created.send_robust(self.__class__, order=order)
            
            return order