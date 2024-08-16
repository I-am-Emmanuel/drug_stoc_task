import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from store.models import Product, Customer

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user_model():
    return get_user_model()

@pytest.mark.django_db
class TestCreateProduct:
    '''This test focus on all product related views api'''

    def test_if_anonymous_user_can_post_a_product_returns_401(self, api_client):
        response = api_client.post('/store/products/', {'title': 'a'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_if_user_can_access_the_product_list_returns_200(self, api_client):
        response = api_client.get('/store/products/')
        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_delete_product_not_associated_with_order(self, api_client, user_model):
        product = Product.objects.create(title='Another Product', description='Another test product', price=15.99, quantity=50)
        api_client.force_authenticate(user=user_model(is_staff=True))
        response = api_client.delete(f'/store/products/{product.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Product.objects.filter(id=product.id).exists()

    def test_admin_cannot_delete_product_associated_with_order(self, api_client, user_model):
        user = user_model.objects.create_user(username='kola', email='emma@gmail.com', password='123456')
        customer = Customer.objects.create(user=user)
        product = Product.objects.create(title='Another Product', description='Another test product', price=15.99, quantity=50)

        api_client.force_authenticate(user=user_model(is_staff=True))
        response = api_client.delete(f'/store/products/{product.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Product.objects.filter(id=product.id).exists()
    
    def test_admin_can_update_the_product_return_200(self, api_client, user_model):
        product = Product.objects.create(title='Another Product', description='Another test product', price=15.99, quantity=50)
        api_client.force_authenticate(user=user_model(is_staff=True))
        response = api_client.put(
            f'/store/products/{product.id}/',
            {'title': 'Updated Product', 'description': 'Updated description', 'price': 20.99, 'quantity': 100}
        )
        assert response.status_code == status.HTTP_200_OK

    def test_if_admin_update_with_wrong_data_return_400(self, api_client, user_model):
        product = Product.objects.create(title='Another Product', description='Another test product', price=15.99, quantity=50)
        api_client.force_authenticate(user=user_model(is_staff=True))
        response = api_client.put(
            f'/store/products/{product.id}/',
            {'title': 'Updated Product', 'description': 'Updated description', 'price': 'wou.8', 'quantity': 0}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST