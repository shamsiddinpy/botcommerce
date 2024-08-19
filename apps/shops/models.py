from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import CASCADE, Model, TextChoices

from apps.shared.django.models import CreatedBaseModel


# Create your models here.
class Category(Model):
    class Status(TextChoices):
        ACTIVE = 'active', 'Active'  # faol
        INACTIVE = 'inactive', 'Inactive'  # harakatsz

    name = models.CharField(max_length=255)
    emoji = models.CharField(max_length=255, null=True, blank=True)
    parent = models.ForeignKey('self', CASCADE, null=True, blank=True, related_name='children')
    show_in_ecommerce = models.BooleanField("Web saytda ko'rsatish", db_default=False)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.INACTIVE)
    description = models.TextField(null=True, blank=True)
    position = models.IntegerField("tartiblash tartibi", default=1)
    shop = models.ForeignKey('shops.Shop', CASCADE, related_name='categories_set')
    attachments = GenericRelation('shops.Attachment', "record_id", blank=True)

    # Rasm jpg, png, jpeg formatda bo'lsa s haffof ko'rinadi 1200x680 px

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kategorya'
        verbose_name_plural = 'Kategorylar'


class ShopCategory(Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Do'koni nomi"
        verbose_name_plural = "Do'koni nomlari"


class Shop(CreatedBaseModel):  # ✅
    class Status(TextChoices):
        ACTIVE = 'active', 'Active'  # Faol
        IN_ACTIVE = 'inactive', 'Inactive'  # Faol emas

    name = models.CharField("Do'kon nomi", max_length=55)
    phone = models.CharField("Biznes telefon raqami", max_length=50)
    phone_number = models.CharField("Telefon raqami", max_length=50)

    country = models.ForeignKey("shops.Country", CASCADE, verbose_name="Ro'yxatdan o'tgan davlat")
    languages = models.ManyToManyField("shops.Language", blank=True, verbose_name="Til")
    services = models.ManyToManyField('orders.Service', through='orders.ShopService')
    shop_category = models.ForeignKey("shops.ShopCategory", CASCADE, verbose_name="Kategoriyalar")
    status = models.CharField(max_length=8, choices=Status.choices, db_default=Status.ACTIVE)
    currency = models.ForeignKey("shops.Currency", CASCADE, verbose_name="Pul birligi")
    plan = models.ForeignKey('users.Plan', CASCADE, related_name='view')
    owner = models.ForeignKey('users.User', CASCADE, related_name='view')
    lat = models.FloatField('Location lat', blank=True, null=True)
    lon = models.FloatField('Location lon', blank=True, null=True)
    starts_at = models.TimeField('Dan', blank=True, null=True)
    ends_at = models.TimeField('Gacha', blank=True, null=True)
    has_terminal = models.BooleanField(db_default=True)
    about_us = models.TextField("Biz haqimizda", null=True, blank=True)
    facebook = models.URLField("Facebook", max_length=255, null=True, blank=True)
    instagram = models.URLField("Instagram", max_length=255, null=True, blank=True)
    telegram = models.URLField('Telegram', max_length=255, null=True, blank=True)
    email = models.URLField("Elektron pochta", max_length=255, null=True, blank=True)
    address = models.CharField('Manzil', max_length=500, null=True, blank=True)
    is_new_products_show = models.BooleanField("'Yangi mahsulotlar' sahifasini ko'rsatish", default=False,
                                               db_default=False)
    is_popular_products_show = models.BooleanField("Ommabop mahsulotlar' sahifasini ko'rsatish", default=False,
                                                   db_default=False)
    attachments = GenericRelation('shops.Attachment', 'record_id', blank=True)
    shop_logo = GenericRelation('shops.Attachment', 'record_id', blank=True)
    favicon_image = GenericRelation('shops.Attachment', 'record_id', blank=True)
    slider_images = GenericRelation('shops.Attachment', 'record_id', blank=True)


class Attachment(CreatedBaseModel):
    content_type = models.ForeignKey('contenttypes.ContentType', CASCADE, null=True, blank=True,
                                     related_name='attachments')
    record_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'record_id')
    key = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(null=True, blank=True)


class TemplateColor(Model):  # ✅
    name = models.CharField(max_length=55, verbose_name='Nomi')
    color = models.CharField(max_length=55, verbose_name='Rangi')

    class Meta:
        verbose_name = 'Shablon rangi'
        verbose_name_plural = 'Shablon ranglari'

    def __str__(self):
        return self.name


class Product(CreatedBaseModel):
    class StockStatus(TextChoices):
        INDEFINITE = 'indefinite', 'Indefinite'  # no aniq
        FIXED = 'fixed', 'Fixed'
        NOT_AVAILABLE = 'not available', 'Not available'

    class Units(TextChoices):
        ITEM = 'item', 'Item'
        WEIGHT = 'weight', 'Weight'

    name = models.CharField(max_length=255, verbose_name='Mahsulotning nomi')
    category = models.ForeignKey('shops.Category', CASCADE, related_name='products',
                                 verbose_name="Kategoriya")
    full_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Mahsulotning umumiy narxi")
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                         verbose_name="Mahsulotning sotib olish narxi")
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=0, verbose_name="Mahsulot soni")
    ikpu_code = models.IntegerField(null=True, blank=True, verbose_name="Mahsulotning IKPU kodi")
    packing_code = models.CharField(max_length=255, null=True, blank=True,
                                    verbose_name="Mahsulotning qadoqlash kodi")
    has_available = models.BooleanField(default=True, verbose_name="Mahsulotning o'ya sah")
    package_code = models.IntegerField('qadoq ko`di', null=True, blank=True)
    stock_status = models.CharField(max_length=100, choices=StockStatus.choices)
    unit = models.CharField(max_length=20, choices=Units.choices, verbose_name="Birligi")
    barcode = models.CharField(max_length=255, null=True, blank=True, verbose_name="Mahsulotning shtrix kodi")
    vat_percent = models.IntegerField('QQS foizi', null=True, blank=True)
    position = models.IntegerField('sort order', db_default=1)

    length = models.IntegerField(blank=True, verbose_name="Mahsulotning uzunligi")
    width = models.IntegerField(blank=True, verbose_name="Mahsulotning kengligi")
    height = models.IntegerField(blank=True, verbose_name="Mahsulotning balandligi")
    weight = models.IntegerField(blank=True, verbose_name="Mahsulotning vazni")

    internal_notes = models.TextField(blank=True, verbose_name="Ichki eslatmalar")
    length_class = models.ForeignKey('shops.Length', CASCADE, verbose_name="Uzunlik birligi",
                                     blank=True, related_name='lengths')
    weight_class = models.ForeignKey('shops.Weight', CASCADE, verbose_name="Vazn birligi",
                                     blank=True, related_name='weights')
    attachments = GenericRelation('shops.Attachment', 'record_id', blank=True)


class Length(Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Weight(Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Attribute(Model):
    name = models.CharField(max_length=50, verbose_name='atribut nomi')
    product = models.ForeignKey('shops.Product', on_delete=models.CASCADE, related_name='attributes',
                                verbose_name="mahsulotlar")

    def __str__(self):
        return self.name


class AttributeValue(Model):
    attribute = models.ForeignKey('shops.Attribute', CASCADE, verbose_name="atribut",
                                  related_name='values')
    value = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="atribut qiymati")

    def __str__(self):
        return self.attribute.name


class AttributeVariant(Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField('Sotuv narxi', max_digits=15, decimal_places=2)
    full_price = models.DecimalField('Umumiy narxi', max_digits=15, decimal_places=2)
    weight_class = models.ForeignKey('shops.Weight', CASCADE, null=True, blank=True, related_name='attribute')
    length_class_id = models.ForeignKey('shops.Length', CASCADE, null=True, blank=True, related_name='attribute')
    weight = models.IntegerField(null=True, blank=True)
    length = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    package_code = models.IntegerField(null=True, blank=True)
    ikpu_code = models.IntegerField(null=True, blank=True)
    stock_status = models.CharField(max_length=20)
    quantity = models.IntegerField(null=True, blank=True)
    unit = models.CharField(max_length=20)
    barcode = models.IntegerField(null=True, blank=True)
    has_available = models.BooleanField(db_default=False)
    vat_percent = models.IntegerField(db_default=0)
    product = models.ForeignKey('shops.Product', CASCADE, related_name='variants')


class Country(Model):
    name = models.CharField(max_length=255, verbose_name='davlatlar nomi')
    code = models.CharField(max_length=255, verbose_name='davlatlar kodi')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Davlat'
        verbose_name_plural = 'Davlatlar'


class Currency(Model):
    name = models.CharField(max_length=255, verbose_name='Nomi')
    order = models.PositiveSmallIntegerField(default=1, db_default=1, verbose_name='rangi')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Pul birlgi'
        verbose_name_plural = 'Pul birlklari'


class Language(Model):
    title = models.CharField(max_length=255, verbose_name='Nomi')
    code = models.CharField(max_length=255, verbose_name='Code')
    icon = models.CharField(max_length=255, blank=True, verbose_name='Bayrog rasmi')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Davlat tili'
        verbose_name_plural = 'Davlat tilari'
