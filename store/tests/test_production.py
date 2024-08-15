from rest_framework.test import APIClient
from rest_framework import status
import pytest
from django.contrib.auth.models import User
from store.models import Product, OrderDetail, Customer


@pytest.mark.django_db
class TestCreateProduct:
    '''This test focus on all product related views api'''
    
    def test_if_user_can_post_a_product_returns_401(self):

        client = APIClient()
        response = client.post('/store/products/', {'title': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_if_user_can_access_the_product_list_returns_200(self):

        client = APIClient()
        response = client.get('/store/products/')
        assert response.status_code == status.HTTP_200_OK

    
    def test_admin_can_delete_product_not_associated_with_order(self):
        
        product = Product.objects.create(title='Another Product', description='Another test product', price=15.99, quantity=50)
        
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response = client.delete(f'/store/products/{product.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not Product.objects.filter(id=product.id).exists()
    
    def test_admin_can_update_the_product_return_201(self):
        product = Product.objects.create(title='Another Product', description='Another test product', price=15.99, quantity=50)
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response = client.put(
        f'/store/products/{product.id}/',
        {'title': 'Updated Product', 'description': 'Updated description', 'price': 20.99, 'quantity': 100}
        )
        assert response.status_code == status.HTTP_200_OK

    def test_if_admin_update_with_wrong_data_return_400(self):
        product = Product.objects.create(title='Another Product', description='Another test product', price=15.99, quantity=50)
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response = client.put(
        f'/store/products/{product.id}/',
        {'title': 'Updated Product', 'description': 'Updated description', 'price': 'wou.8', 'quantity': 0}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST