# Register your models here.


from django.contrib import admin

from shops.models import Category, Product, ShopCategory, Shop, Attachment, TemplateColor, Length, Weight, Attribute, \
    AttributeValue, AttributeVariant, Country, Currency, Language


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(ShopCategory)
class ShopCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    pass


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    pass


@admin.register(TemplateColor)
class TemplateColorAdmin(admin.ModelAdmin):
    pass


@admin.register(Length)
class LengthAdmin(admin.ModelAdmin):
    pass


@admin.register(Weight)
class WeightAdmin(admin.ModelAdmin):
    pass


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    pass


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    pass


@admin.register(AttributeVariant)
class AttributeVariantAdmin(admin.ModelAdmin):
    pass


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass
