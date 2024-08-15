from django.db.models import Count, F, Sum
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework import status
from rest_framework.response import Response
from .serializers import ProductSerializer, CustomerSerializer, UpdateCartItemSerializer, CartSerializer, CartItemSerializer, AddCartItemSerializer, OrderSerializer, CreateOrderSerializer, UpdateOrderSerializer
from .models import Product, OrderDetail, Cart, CartItem, Customer, Order
from .permission import IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .filter import ProductQuantityFilter
from rest_framework.views import APIView
from django.utils import timezone


# View_set api's
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductQuantityFilter

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderDetail.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Products cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)    

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods= ['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == 'GET':

        # request.user # This wil be sent to Anonymous User Class
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer
    
class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    # query_set = CartItem
    # serializer_class = CartItemSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer

        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer 
        return CartItemSerializer
         
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])\
                                .select_related('product')



class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()

        customer_id = Customer.objects.only(
            'id').get(user_id=user)
        return Order.objects.filter(customer_id=customer_id)



class SalesReportView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, format=None):
        period = request.query_params.get('period', 'days')

        if period == 'day':
            start_date = timezone.now() - timezone.timedelta(days=1)
        elif period == 'week':
            start_date = timezone.now() - timezone.timedelta(weeks=1)
        elif period == 'month':
            start_date = timezone.now() - timezone.timedelta(days=30)
        elif period == '5min':
            start_date = timezone.now() - timezone.timedelta(minutes=5)
        else:
            return Response({"error": "Invalid period"}, status=status.HTTP_400_BAD_REQUEST)

        completed_orders = Order.objects.filter(
            placed_at__gte=start_date, order_status=Order.COMPLETED_ORDER
        )

        # Calculate the total sales for the filtered orders
        total_sales = completed_orders.annotate(
            item_total=F('items__quantity') * F('items__unit_price')
        ).aggregate(total_sales=Sum('item_total'))['total_sales']

        serializer = OrderSerializer(completed_orders, many=True)

        # Return the response with total sales and order data
        return Response({
            "total_sales": total_sales,
            "orders": serializer.data
        }, status=status.HTTP_200_OK)


# class ProductQuantityListView(APIView):
#     def get(self, request):
#         quantity_lt = request.query_params.get('quantity_lt', 10)  
#         products = Product.objects.filter(quantity__lt=quantity_lt)
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)
