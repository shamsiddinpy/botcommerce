from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import (CASCADE, RESTRICT, SET_NULL, ManyToManyField,
                              TextChoices)
from shared.django.models import CreatedBaseModel
from users.managers import CustomUserManager


class Person(models.Model):
    name = models.CharField(max_length=100, verbose_name='mijozning ismi')
    phone = models.CharField(max_length=100, verbose_name='mijozning telfoni raqmi')

    def __str__(self):
        return self.name


class ShopUser(AbstractBaseUser):
    class Type(TextChoices):
        EMAIL = 'email', 'Email'
        TELEGRAM = 'telegram', 'Telegram'
        FACEBOOK = 'facebook', 'Facebook'

    username = models.CharField(max_length=100, unique=True, validators=[UnicodeUsernameValidator])
    person = models.OneToOneField('users.Person', SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=255)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    last_activity = models.DateTimeField(auto_now_add=True)
    is_blocked = models.BooleanField(db_default=False)
    created_at = models.DateTimeField(auto_now=True)
    language = models.ForeignKey('shops.Language', CASCADE, null=True)
    shop = models.ForeignKey('shops.Shop', CASCADE, related_name='customers')

    objects = UserManager()

    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        unique_together = [
            ('username', 'shop')
        ]


class User(AbstractBaseUser, PermissionsMixin):
    class Type(TextChoices):
        EMAIL = 'email', 'Email'
        TELEGRAM = 'telegram', 'Telegram'
        FACEBOOK = 'facebook', 'Facebook'

    type = models.CharField(max_length=255)
    username = models.CharField('foydalanuvchini nomi', max_length=100, blank=True, null=True, unique=True,
                                validators=[UnicodeUsernameValidator])
    email = models.EmailField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    language = models.ForeignKey('shops.Language', CASCADE, null=True)
    public_offer = models.BooleanField(default=False)
    invitation_code = models.CharField(max_length=100, unique=True, null=True)
    default_shop = models.ForeignKey('shops.Shop', CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'


class Plan(CreatedBaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    code = models.CharField(max_length=100, verbose_name='qaysi tarfidan foydalanyotgani')
    quotas = ManyToManyField('users.Quotas')

    def __str__(self):
        return f"{self.name} "


class PlanPricing(CreatedBaseModel):
    class PeriodType(TextChoices):
        MONTHLY = 'monthly', 'Monthly'  # OYLIK
        YEARLY = 'yearly', 'Yearly'  # YILIK

    name = models.CharField(max_length=100)
    currency = models.ForeignKey('shops.Currency', RESTRICT)
    period_type = models.IntegerField('Davr turi', choices=PeriodType.choices)
    price = models.PositiveIntegerField('Narxi')
    original_price = models.PositiveIntegerField('Haqiqiy narxi')
    period = models.IntegerField('davr')
    plan = models.ForeignKey('users.Plan', CASCADE, )

    def __str__(self):
        return f"{self.name}+{self.period_type}"


class Quotas(CreatedBaseModel):
    name = models.CharField('Kvotalar Nome', max_length=100)
    description = models.TextField('Kvotalar Tavsif')

    def __str__(self):
        return f"{self.name} "


class PlanQuotas(models.Model):
    plan = models.ForeignKey('users.Plan', CASCADE)
    quotas = models.ForeignKey('users.Quotas', CASCADE)
    value = models.CharField('Qiymat', max_length=50)


class PlanInvoice(CreatedBaseModel):  # ✅
    class Status(TextChoices):
        NEW = 'new', 'New'
        COMPLETED = 'completed', 'Completed'

    price = models.CharField('Narxi', max_length=55)
    user = models.ForeignKey('users.User', CASCADE, related_name='plan_invoices')
    plan = models.ForeignKey('users.Plan', CASCADE)
    payed_at = models.DateTimeField('da toʻlangan', null=True, blank=True)
    pay_url = models.URLField('tolov url', null=True, blank=True)
    plan_extended_from = models.DateField()
    plan_extended_until = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=25, choices=Status.choices, db_default=Status.NEW)
