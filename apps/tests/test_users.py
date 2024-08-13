import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db
class TestUserShopUrl:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    def test_register_user(self, api_client):
        url = reverse('register')
        assert url == '/api/v1/users/sign-up'

    def test_login_user(self, api_client):
        url = reverse('login')
        assert url == '/api/v1/users/login'

    def test_logout_user(self, api_client):
        url = reverse('logout')
        assert url == '/api/v1/users/logout'

    def test_register(self, api_client):
        url = reverse('register')
        data = {
            'first_name': 'Shamsiddin',
            'last_name': 'Daminov',
            'email': 'shamsiddin@gmail.com',
            'password': '1',
            'confirm_password': '1',
            'type': 'email',
            'invitation_code': '1'
        }
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert User.objects.filter(email='shamsiddin@gmail.com').exists()

    def test_login(self, api_client):
        if not User.objects.filter(email='shamsiddin@gmail.com').exists():
            user = User.objects.create_user(email='shamsiddin@gmail.com', password='1')
            user.is_active = True
            user.save()
        url = reverse('login')
        data = {
            'email': 'shamsiddin@gmail.com',
            'password': '1',
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data


