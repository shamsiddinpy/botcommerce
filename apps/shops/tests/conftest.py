import pytest
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from shops.models import Country, ShopCategory, Currency, Shop, Product, Category
from users.models import User, Plan


@pytest.fixture(scope='function')
def user1():
    data = {
        'email': 'user1@gmail.com',
        'password': '1',
        'is_active': True,
        'is_superuser': False,
        'is_staff': True,
        'type': 'email'
    }
    return User.objects.create_user(**data)


@pytest.fixture(scope='function')
def user2():
    data = {
        'email': 'user2@gmail.com',
        'password': '1',
        'is_active': True,
        'is_superuser': False,
        'is_staff': True,
        'type': 'email'
    }
    return User.objects.create_user(**data)


@pytest.fixture(scope='function')
def login_user1(client, user1):
    client = APIClient()
    client.force_authenticate(user=user1)
    return client


@pytest.fixture(scope='function')
def login_user2(client, user2):
    client = APIClient()
    client.force_authenticate(user=user2)
    return client


@pytest.fixture(scope='function')
def country():
    return Country.objects.create(name='Uzbekistan', code='uz')


@pytest.fixture(scope='function')
def shop_category():
    return ShopCategory.objects.create(name='Texnika1')


@pytest.fixture(scope='function')
def currency():
    return Currency.objects.create(name='Sum', order=1)


@pytest.fixture(scope='function')
def plan():
    return Plan.objects.create(name='Free', code='free', description='Free dan foydalanyapsiz')


@pytest.fixture(scope='function')
def shop(user1, country, shop_category, currency, plan):
    shop = Shop.objects.create(
        name="Shop test",
        phone="+998908840720",
        phone_number='8989898',
        status="active",
        lat=7878700.12,
        lon=7878700.12,
        starts_at=None,
        ends_at=None,
        has_terminal=True,
        about_us="Biz haqimizda malumot",
        facebook="https://facebook.com",
        instagram="https://instagram.com",
        telegram="https://telegram.com",
        email="shop1@gmail.com",
        address="Tashkent sh",
        is_new_products_show=True,
        is_popular_products_show=True,
        country=country,
        shop_category=shop_category,
        currency=currency,
        owner=user1,
        plan=plan,
    )
    user1.default_shop = shop
    return shop


@pytest.fixture(scope='function')
def shop1(user1, country, shop_category, currency, plan):
    return Shop.objects.create(
        name="Shop test",
        phone="+998908840720",
        phone_number='8989898',
        status="active",
        lat=7878700.12,
        lon=7878700.12,
        starts_at=None,
        ends_at=None,
        has_terminal=True,
        about_us="Biz haqimizda malumot",
        facebook="https://facebook.com",
        instagram="https://instagram.com",
        telegram="https://telegram.com",
        email="shop1@gmail.com",
        address="Tashkent sh",
        is_new_products_show=True,
        is_popular_products_show=True,
        country=country,
        shop_category=shop_category,
        currency=currency,
        owner=user1,
        plan=plan,
    )


@pytest.fixture(scope='function')
def shop2(user2, country, shop_category, currency, plan):
    shop2 = Shop.objects.create(
        name="Shop2 test",
        phone="+998908840720",
        phone_number='8989898',
        status="active",
        lat=7878700.12,
        lon=7878700.12,
        starts_at=None,
        ends_at=None,
        has_terminal=True,
        about_us="Biz haqimizda malumot",
        facebook="https://facebook.com",
        instagram="https://instagram.com",
        telegram="https://telegram.com",
        email="shamsiddin@gmail.com",
        address="Tashkent sh",
        is_new_products_show=True,
        is_popular_products_show=True,
        country=country,
        shop_category=shop_category,
        currency=currency,
        owner=user2,
        plan=plan,
    )
    user2.default_shop = shop2
    return shop2


@pytest.fixture(scope='function')
def category(shop):
    return Category.objects.create(
        name='Texnika',
        emoji='🤑',
        position=2,
        status='active',
        shop=shop
    )


@pytest.fixture(scope='function')
def category1(shop2):
    return Category.objects.create(
        name='Texnika',
        emoji='🤑',
        position=2,
        status='active',
        shop=shop2
    )


@pytest.fixture(scope='function')
def category2(shop):
    return Category.objects.create(
        name='Iphone 11 pro',
        emoji='🤑',
        position=2,
        status='active',
        shop=shop
    )


@pytest.fixture(scope='function')
def product(category):
    return Product.objects.create(
        name='Product 1',
        description='chotki',
        category=category,
        full_price=124,
        price=12,
        stock_status='fixed',
        unit='item'
    )


@pytest.fixture(scope='function')
def product1(category1):
    return Product.objects.create(
        name='Product 2',
        description='chotki',
        category=category1,
        full_price=124,
        price=12,
        stock_status='fixed',
        unit='item'
    )


@pytest.fixture(scope='function')
def product2(category):
    return Product.objects.create(
        name='Mahsulot 1',
        description='chotki',
        category=category,
        full_price=124,
        price=12,
        stock_status='fixed',
        unit='item'
    )
