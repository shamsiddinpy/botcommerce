from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import CASCADE, RESTRICT, SET_NULL, Model, TextChoices
from shared.django.models import CreatedBaseModel
from shops.models import Currency
from users.models import User


class Order(CreatedBaseModel):
    class Status(TextChoices):
        ACCEPTED = 'accepted', 'Accepted'  # qabul qilingan
        CONFIRMED = 'confirmed', 'Confirmed'  # Tasdiqlandi
        IN_PROGRESS = 'in_progress', 'In_progres'  # jarayonda
        SUCCESSFULLY = 'successfully', 'Successfully'  # Muvaffaqiyatli
        CANCELED = 'Canceled', 'Canceled'  # bekor qilindi
        PAYMENT_CANCELLED = "payment cancelled", "Payment Cancelled"  # to'lov bekor qilindi
        RETURNED = 'returned', 'Returned'  # qaytarildi

    class Type(TextChoices):
        TELEGRAM = 'telegram', 'Telegram'
        WEB = 'web', 'Web'
        WHATSAPP = 'whatsapp', 'Whatsapp'

    class DeliveryType(TextChoices):
        TAKE_AWAY = 'take away', 'Take away'  # Olib ketish
        DELIVERY = 'delivery', 'Delivery'  # yetkazib berish
        ONLINE_DELIVERY = 'online delivery', 'Online Delivery'  # onlyin yetkazib berish

    currency = models.ForeignKey('shops.Currency', RESTRICT, related_name='orders')
    user = models.ForeignKey('users.ShopUser', CASCADE)
    person = models.ForeignKey('users.Person', CASCADE, related_name='orders')
    promo_code = models.ForeignKey('orders.PromoCode', SET_NULL, null=True, blank=True, related_name='orders')

    delivery_date = models.DateField(blank=True, null=True, verbose_name='yetkazib berish sanasi')
    delivery_type = models.CharField(max_length=20, choices=DeliveryType.choices)
    delivery_price = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10,
                                         verbose_name='yetkazib berish narxi ')

    is_archived = models.BooleanField(default=False, verbose_name='arxivdagi zakaslar')
    note = models.TextField(blank=True, null=True, verbose_name='usering fikri')

    order_type = models.CharField(choices=Type.choices, max_length=20)
    paid = models.BooleanField(db_default=False, verbose_name="To'lov qilingan yoki yo'qligi")
    shop_service = models.ForeignKey('orders.ShopService', CASCADE)
    status = models.CharField(choices=Status.choices, max_length=20)
    total_price = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10,
                                      verbose_name='umumiy narxi')
    door_phone = models.CharField(blank=True, null=True, max_length=20, verbose_name='domni nomiri')
    floor_number = models.IntegerField('Qavat raqami', null=True, blank=True)
    address = models.CharField(blank=True, null=True, max_length=255, verbose_name='manzil')
    apartment_number = models.IntegerField('kvartera raqami', null=True, blank=True)

    lon = models.FloatField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    first_name = models.CharField(blank=True, null=True, max_length=20)
    last_name = models.CharField(blank=True, null=True, max_length=20)
    email = models.EmailField(blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class PromoCode(Model):
    class Types(TextChoices):
        FREE_DELIVERY = 'free_delivery', 'Free_delivery'  # Bepul yetkazib berish
        DISCOUNT = 'discount', 'Discount'  # chegirma

    type = models.CharField(max_length=20, choices=Types.choices, verbose_name='Promo kodi turi')
    code = models.CharField(max_length=255, unique=True, verbose_name='Kod')
    amount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Foydalanish miqdori')
    shop = models.ForeignKey('shops.Shop', on_delete=models.CASCADE, verbose_name='Do\'kon')
    percent = models.IntegerField(default=0, verbose_name='Chegirma foizi')
    limit = models.IntegerField(verbose_name='promode cheklash vaqti')
    starts_at = models.DateField(verbose_name=' promocde boshlash vaqti')
    ends_at = models.DateField(verbose_name='promo code tugash vaqti ')
    is_active = models.BooleanField(default=False)
    code = models.CharField(max_length=255)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Promo kod'
        verbose_name_plural = 'Promo kodlar'
        unique_together = (('shop', 'code'),)


class OrderItem(Model):
    order = models.ForeignKey('orders.Order', CASCADE, related_name='items')
    count = models.PositiveIntegerField(db_default=1)
    currency = models.ForeignKey('shops.Currency', CASCADE)
    product_attribute = models.ForeignKey('shops.AttributeVariant', CASCADE, related_name='promo_code')


class ShopService(Model):
    class Status(TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        NOT_EXISTS = 'not_exists', 'Not exists'

    shop = models.ForeignKey('shops.Shop', CASCADE)
    service = models.ForeignKey('orders.Service', CASCADE)
    status = models.CharField(max_length=15, choices=Status.choices, db_default=Status.INACTIVE)
    fields = models.ManyToManyField('orders.Field', through='orders.ShopServiceField')

    def __str__(self):
        return f'{self.shop} {self.service}'


class ShopServiceField(Model):
    shop_service = models.ForeignKey('orders.ShopService', CASCADE)
    field = models.ForeignKey('orders.Field', CASCADE)
    value = models.JSONField(default=dict)


class Field(Model):
    class Type(TextChoices):
        INTEGER = 'integer', 'Integer'  # butun son
        STRING = 'string', 'String'
        TEXT = 'text', 'Text'
        LIST = 'list', 'List'
        VIDEO = 'video', 'Video'
        IMAGE = 'image', 'Image'
        GEOLOCATION = 'geolocation', 'Geolocation'  # Geolokatsiya

    service = models.ForeignKey('orders.Service', CASCADE, related_name='fields')
    label = models.CharField(max_length=255)
    name = models.CharField(max_length=255, unique=True)
    max_length = models.IntegerField()
    required = models.BooleanField()
    type = models.CharField(max_length=255, choices=Type.choices)
    provider_labels = models.JSONField(null=True, blank=True)


class Service(Model):
    class ServiceType(TextChoices):
        DELIVERY = 'delivery', 'Delivery'  # yetkazib berish
        PAYMENT = 'payment', 'Payment'  # To'lov

    class Type(TextChoices):
        INTERNAL = 'internal', 'Internal'  # ichki
        INPLACE = 'inplace', 'Inplace'  # joyida
        TELEGRAM = 'telegram', 'Telegram'  # teligram
        WEB = 'web', 'Web'  # Veb
        INSTALMENT = 'instalment', 'Instalment'  # to'lov

    service_type = models.CharField(max_length=15, choices=ServiceType.choices)
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=Type.choices)
    description = models.TextField(null=True, blank=True)
    attachments = GenericRelation('shops.Attachment', 'record_id', blank=True)

    class Meta:
        unique_together = [
            ('code', 'type')
        ]
