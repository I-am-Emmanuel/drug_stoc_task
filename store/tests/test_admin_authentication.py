from rest_framework.test import APIClient
from rest_framework import status
import pytest
from django.contrib.auth.models import User

@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
class TestUsersAuthentication:

    def test_if_no_admin_user_view_ordered_endpoint_returns_403(self, client):
        client.force_authenticate(user={})
        response = client.get('/store/orders/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_no_admin_user_view_customer_endpoint_returns_403(self, client):
        client.force_authenticate(user={})
        response = client.get('/store/customers/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_if_no_admin_user_view_sales_report_returns_403(self, client):
        client.force_authenticate(user={})
        response = client.get('/store/sales-report/?period=days')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    


