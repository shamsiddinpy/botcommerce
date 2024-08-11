# import pytest
#
# from shops.models import Language, Shop, Country
#
#
# @pytest.fixture
# def language(self):
#     return Language.objects.create(title="English", code="en", icon="🇺🇸")
#
#
# @pytest.fixture
# def country(self):
#     return Country.objects.create(code="US", name="United States")
#
#
# @pytest.fixture
# def shop(self, country, language):
#     return Shop.objects.create(
#         name="Test Shop",
#         phone='908840720',
#         phone_number='908840720',
#         country=country.id,
#         language=language.id,
#
#     )
#
#
# @pytest.fixture
# def user():
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db
class TestUserUrl:
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

    def test_activate_user(self, api_client):
        url = reverse('activate_user')
        assert url == '/api/v1/users/activate_user'

    def test_forgot_password(self, api_client):
        url = reverse('forgot_password')
        assert url == '/api/v1/users/forgot_password'

    def test_reset_password_token_url(self, api_client):
        url = reverse('reset_password_token')
        assert url == '/api/v1/users/reset_password_token'

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
            User.objects.create_user(email='shamsiddin@gmail.com', password='1')
            url = reverse('login')
            data = {
                'email': 'shamsiddin@gmail.com',
                'password': '1',

            }
            response = api_client.post(url, data)
            assert response.status_code == 201
            assert 'token' in response.data
