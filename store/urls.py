from django.urls import path
from django.urls.conf import include
# from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers 
from . import views


router = routers.DefaultRouter()

router.register('products', views.ProductViewSet, basename='products')
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)
router.register('customers-orders', views.CustomerPurchasedHistory, basename='customer-history')
router.register('orders', views.OrderViewSet, basename='orders')

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
carts_router =  routers.NestedDefaultRouter(router, 'carts', lookup= 'cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items-detail')

urlpatterns = [    
    # path('', include(router.urls + products_router.urls)),
    path('', include(router.urls + products_router.urls + carts_router.urls)),
    path('sales-report/', views.SalesReportView.as_view(), name='sales-report'),
    path('lesser-product-report/', views.ProductQuantityListView.as_view(), name='sales-report')
]