import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.shops.tests.conftest import shop, user1, country, currency, shop_category, login_user1


# pytestmark = pytest.mark.django_db

@pytest.mark.django_db
class TestShopView:
    def test_create_shops(self, shop, plan, user1, country, currency, shop_category, client, login_user1):
        url = reverse_lazy('shops:shop-list')
        data = {
            "name": "Shop test",
            "phone": "+998908840720",
            "phone_number": "+998908840720",
            "status": "active",
            "lat": 7878700.12,
            "lon": 7878700.12,
            "has_terminal": True,
            "about_us": "Biz haqimizda malumot",
            "facebook": "https://facebook.com",
            "instagram": "https://instagram.com",
            "telegram": "https://telegram.com",
            "email": "shamsiddin@gmail.com",
            "address": "Tashkent sh",
            "is_new_products_show": True,
            "plan": plan.id,
            "is_popular_products_show": True,
            "country": country.id,
            "shop_category": shop_category.id,
            "currency": currency.id,
            "owner": user1.id,
        }
        response = client.post(url, data)
        assert response.status_code == 201
        response_data = response.data
        assert response_data['name'] == data['name']
        assert response_data['phone_number'] == data['phone_number']
        assert shop.owner_id == user1.id
        assert shop.owner.email == user1.email
        assert shop.owner.type == user1.type
        assert response_data['currency'] == data['currency']
        assert response_data['shop_category'] == shop_category.name

    def test_get_shop(self, user1, client, shop, shop1, login_user1):
        url = reverse_lazy('shops:shop-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        response = login_user1.get(url)
        assert response.status_code == status.HTTP_200_OK
        response_data = response.data
        # assert response_data['id'] == 1

    # @pytestmark
    # def test_shop_detail(self, user1, client, country, currency, shop, plan, shop_category, login_user1, login_user2):
    #     url = reverse_lazy('shops:shop-detail', kwargs={'pk': shop.id})
    #     data = {
    #         "name": "Shop update put",
    #         "phone": "+998908840720",
    #         "phone_number": "8989898",
    #         "status": "active",
    #         "lat": 7878700.12,
    #         "lon": 7878700.12,
    #         "has_terminal": True,
    #         "about_us": "Biz haqimizda malumot",
    #         "facebook": "https://facebook.com",
    #         "instagram": "https://instagram.com",
    #         "telegram": "https://telegram.com",
    #         "email": "user1@gmail.com",
    #         "address": "Tashkent Sh",
    #         "is_new_products_show": True,
    #         "is_popular_products_show": True,
    #         "country": country.id,
    #         "currency": currency.id,
    #         'plan': plan.id,
    #         "shop_category": shop_category.id,
    #     }
    #     response = client.get(url)
    #     assert response.status_code == status.HTTP_401_UNAUTHORIZED
    #     response = login_user1.get(url, data)
    #     assert response.status_code == status.HTTP_200_OK
    #     assert response.data['name'] == shop.name
    #
    #     response = login_user1.get(url, data)
    #     assert response.status_code == status.HTTP_200_OK
    #
    #     response = login_user1.put(url, data)
    #     assert response.status_code == status.HTTP_200_OK
    #     shop.refresh_from_db()
    #     assert response.data['name'] == shop.name
    #
    #     response = login_user1.patch(url, data)
    #     assert response.status_code == status.HTTP_200_OK
    #     assert response.data['name'] == shop.name
    #
    #     response = login_user1.delete(url, data)
    #     assert response.status_code == status.HTTP_204_NO_CONTENT
    #
    #     # response = login_user2.get(url)
    #     # assert response.status_code == status.HTTP_403_FORBIDDEN
