from rest_framework.test import APIClient
from rest_framework import status
import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user_model():
    return get_user_model()
@pytest.mark.django_db
class TestUsersAuthentication:

    def test_login_with_weak_password_fails(self, user_model, client):
        try:
            validate_password('123456')
            user = user_model.objects.create_user(username='kola', email='emma@gmail.com', password='123456')
        except ValidationError as e:
            print(f"Password validation error: {e}")
        
        response = client.post('/auth/jwt/create/', {'username': 'kola', 'password': '123456'})
        
        assert response.status_code != status.HTTP_200_OK
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_401_UNAUTHORIZED]

    def test_for_login_credentials_that_return_200(self, user_model, client):
        user = user_model.objects.create_user(username='kola', email='emma@gmail.com', password='@#(g^hyavsh92')
        response = client.post('/auth/jwt/create/', {'username': 'kola', 'password': '@#(g^hyavsh92'})
        
        assert response.status_code == status.HTTP_200_OK