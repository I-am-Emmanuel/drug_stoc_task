import pytest
from django.contrib.auth import get_user_model
from store.models import Product, Cart
from rest_framework.test import APIClient
from rest_framework import status
from store.models import Cart, Product

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user_model():
    return get_user_model()


@pytest.mark.django_db
class TestCartItem:

    def test_for_anonymous_user_can_get_a_shopping_cart_return_201(self, client):
        response = client.post('/store/carts/')
        assert response.status_code == status.HTTP_201_CREATED

    def test_for_registered_user_cannot_get_a_shopping_cart_return_404(self, client):
        client.force_authenticate(user={})
        response = client.post('/store/carts/')
        assert response.status_code != status.HTTP_401_UNAUTHORIZED

    def test_for_anonymous_user_that_get_cart_can_access_items(self, client):
        
        response = client.post('/store/carts/')
        
        _id = response.data.get('id')
        response = client.get(f'/store/carts/{_id}/items/')
        print(f"Response Data: {response.data}")
            
        assert response.status_code == status.HTTP_200_OK

    def test_for_authenticated_user_that_get_cart_can_access_items(self, client):
        client.force_authenticate(user={})
        response = client.post('/store/carts/')
        
        _id = response.data.get('id')
        response = client.get(f'/store/carts/{_id}/items/')
        print(f"Response Data: {response.data}")
            
        assert response.status_code == status.HTTP_200_OK
    
    def test_for_authenticated_user_that_cannot_add_non_existing_product_to_the_cart(self, client):
        client.force_authenticate(user={})
        response = client.post('/store/carts/')
        assert response.status_code == status.HTTP_201_CREATED, f"Failed to create cart: {response.data}"
        
        cart_id = response.data.get('id')

        response = client.post(
            f'/store/carts/{cart_id}/items/',
            {'product_id': 9999, 'quantity': 10}  
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        
    def test_for_authenticated_user_that_can_add_existing_product_to_the_cart(self, client):

        client.force_authenticate(user={})

        product = Product.objects.create(title='Sample Product', description='Sample description', price=10.00, quantity=100)

        response = client.post('/store/carts/')
        assert response.status_code == status.HTTP_201_CREATED, f"Failed to create cart: {response.data}"
        
        cart_id = response.data.get('id')

        response = client.post(
            f'/store/carts/{cart_id}/items/',
            {'product_id': product.id, 'quantity': 10}
        )
        assert response.status_code == status.HTTP_201_CREATED, f"Failed to add item: {response.data}"

        