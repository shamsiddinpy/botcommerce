import random

from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from shops.models import (Category, Country, Currency, Product, Shop,
                          ShopCategory)
from users.models import Plan, User


class Command(BaseCommand):
    help = 'Generates N fake records for specified model'

    def add_arguments(self, parser):
        parser.add_argument('model', type=str, help='Model to populate: user, shop, category, product')
        parser.add_argument('n', type=int, help='Number of fake records to create')

    def handle(self, *args, **kwargs):
        model, n = kwargs['model'].lower(), kwargs['n']
        fake = Faker()

        # Create necessary objects first
        self.create_initial_objects(fake)

        creators = {'user': self.create_fake_users, 'shop': self.create_fake_shops,
                    'category': self.create_fake_categories}
        if model in creators:
            creators[model](n, fake)
        else:
            raise CommandError('Invalid model. Use: user, shop, category, product')

    def create_initial_objects(self, fake):
        # Create countries
        for _ in range(5):
            Country.objects.create(name=fake.country())

        # Create currencies
        for _ in range(3):
            Currency.objects.create(name=fake.currency_code())

        # Create plans
        for _ in range(3):
            Plan.objects.create(name=fake.word(), description=fake.sentence(), code=fake.word())

        # Create users (if not exists)
        if not User.objects.exists():
            self.create_fake_users(5, fake)

        # Create shop categories
        for _ in range(5):
            ShopCategory.objects.create(name=fake.word())

    def create_fake_users(self, n, fake):
        for _ in range(n):
            user = User.objects.create(
                username=fake.unique.user_name(),
                email=fake.unique.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )
            user.set_password('password123')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created User: {user.username}'))

    def create_fake_shops(self, n, fake):
        countries = list(Country.objects.all())
        categories = list(ShopCategory.objects.all())
        currencies = list(Currency.objects.all())
        plans = list(Plan.objects.all())  # Make sure this is not empty
        users = list(User.objects.all())

        if not plans:
            raise CommandError('No plans found. Createw plans first')

        for _ in range(n):
            shop = Shop.objects.create(
                name=fake.company(),
                phone=fake.phone_number(),
                phone_number=fake.phone_number(),
                country=random.choice(countries),
                shop_category=random.choice(categories),
                status=random.choice(Shop.Status.values),
                currency=random.choice(currencies),
                owner=random.choice(users),
                plan=random.choice(plans),  # Add plan here
                lat=fake.latitude(),
                lon=fake.longitude(),
                starts_at=fake.time_object(),
                ends_at=fake.time_object(),
                has_terminal=fake.boolean(),
                about_us=fake.paragraph(nb_sentences=3),
                facebook=fake.url(),
                instagram=fake.url(),
                telegram=fake.url(),
                email=fake.email(),
                address=fake.address(),
                is_new_products_show=fake.boolean(),
                is_popular_products_show=fake.boolean(),
            )
            self.stdout.write(self.style.SUCCESS(f'Created Shop: {shop.name}'))

    def create_fake_categories(self, n, fake):
        shops = list(Shop.objects.all())
        if not shops:
            raise CommandError('No shops found. Create shops first')

        for _ in range(n):
            category = Category.objects.create(
                name=fake.word().capitalize(),
                emoji=fake.emoji(),
                show_in_ecommerce=fake.boolean(),
                status=random.choice(Category.Status.values),
                description=fake.paragraph(nb_sentences=3),
                position=random.randint(1, 100),
                shop=random.choice(shops),
            )
            self.stdout.write(self.style.SUCCESS(f'Created Category: {category.name}'))

    def create_faker_products(self, n, fake):
        products = list(Product.objects.all())
        categories = list(Category.objects.all())

        if not categories:
            raise CommandError('Kategoriya topilmadi')

        for _ in range(n):
            Product.objects.create(
                name=fake.word().capitalize(),
                category=random.choice(categories),
                full_price=fake.pydecimal(left_digits=5, right_digits=2, positive=True),
                purchase_price=fake.pydecimal(left_digits=5, right_digits=2, positive=True),
                description=fake.text(),
                quantity=fake.random_int(min=1, max=100),
                ikpu_code=fake.random_int(min=1000, max=9999),
                packing_code=fake.word(),
                has_available=fake.boolean(),
                stock_status=random.choice(
                    [Product.StockStatus.INDEFINITE, Product.StockStatus.FIXED, Product.StockStatus.NOT_AVAILABLE]),
                unit=random.choice([Product.Units.ITEM, Product.Units.WEIGHT]),
                barcode=fake.ean13(),
                vat_percent=fake.random_int(min=0, max=25),
                position=fake.random_int(min=1, max=10),
                length=fake.random_int(min=1, max=100),
                width=fake.random_int(min=1, max=100),
                height=fake.random_int(min=1, max=100),
                weight=fake.random_int(min=1, max=100),
                internal_notes=fake.text(),
                length_class=None,  # Agar length_class mavjud bo'lsa, uni moslashtiring
                weight_class=None,  # Agar weight_class mavjud bo'lsa, uni moslashtiring
            )
