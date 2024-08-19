import pytest
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status

from shops.models import (Attachment, Country, Currency, Language, Shop,
                          ShopCategory)
from users.models import Plan, Quotas, User


@pytest.fixture(scope='function')
def language(self):
    return Language.objects.create(title="Uzbek", code="en", icon="🇺🇿")


@pytest.fixture(scope='function')
def country(self):
    return Country.objects.create(code="UZ", name="Uzbekistan")


@pytest.fixture(scope='function')
def shop_category(self):
    return ShopCategory.objects.create(name="Shop1")


@pytest.fixture(scope='function')
def currency(self):
    return Currency.objects.create(name="UZS")


@pytest.fixture(scope='function')
def quotas(self):
    quota1 = Quotas.objects.create(name="Quota 1", description="Description for quota 1")
    quota2 = Quotas.objects.create(name="Quota 2", description="Description for quota 2")
    return [quota1, quota2]


@pytest.fixture(scope='function')
def plan(self, quotas):
    plans = Plan.objects.create(
        name="Basic Plan", description="A basic plan", code="basic"
    )
    plans.quotas.set(quotas)
    return plans


@pytest.fixture(scope='function')
def user(self):
    return User.objects.create_user(email='shamsiddin@gmail.com', password="1")


@pytest.fixture(scope='function')
def attachment(self):
    return Attachment.objects.create(
        content_type=ContentType.objects.get_for_model(Shop),
        record_id=1,
        key='sample_attachment',
        url='https://example.com/sample.jpg'
    )


@pytest.fixture(scope='function')
def shop(self, country, language, shop_category, currency, plan, user, attachment):
    shops = Shop.objects.create(
        name="Test Shop",
        phone='908840720',
        phone_number='908840720',
        country=country,
        shop_category=shop_category,
        currency=currency,
        status=Shop.Status.ACTIVE,
        plan=plan,
        owner=user,
        lat=40.7128,
        lon=-74.0060,
        starts_at='09:00',
        ends_at='18:00',
        has_terminal=True,
        about_us='Biz haqimizda',
        facebook='https://www.facebook.com/testshop',
        instagram='https://www.instagram.com/testshop',
        telegram='https://t.me/testshop',
        email='shamsiddin@gmail.com',
        address='Toshkent Sh',
        is_new_products_show=True,
        is_popular_products_show=True
    )
    shops.attachments.add(attachment)
    shops.shop_logo.add(attachment)
    shops.favicon_image.add(attachment)
    shops.slider_images.add(attachment)
    return shops  # Todo qaytib kelman


@pytest.fixture(scope='function')
def test_create(self, client, shop, country, language, shop_category, currency, plan, user):
    url = reverse('shops:shop-create')
    data = {
        'name': 'New Shop',
        'phone_number': '123456789',
        'languages': [language.id],
        'shop_category': shop_category.id,
        'email': 'newshop@gmail.com',
        'country': country.id,
        'currency': currency.id,
    }
    self.client.force_authenticate(user=user)
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    shop = Shop.objects.get(id=response.data['id'])
    assert shop.name == 'New Shop'
    assert shop.phone_number == '123456789'
    assert shop.country == country.id
    assert shop.currency == currency.id  # Todo qaytib kelman
