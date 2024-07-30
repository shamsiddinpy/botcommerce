from rest_framework.fields import CurrentUserDefault, HiddenField
from rest_framework.serializers import ModelSerializer

from shops.models import Shop, Currency, ShopCategory, Language, Country


class ShopModelSerializer(ModelSerializer):
    owner = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Shop
        fields = 'id', 'name', 'phone_number', 'category', 'country', 'languages', 'currency', 'owner'


class CurrencyModelSerializer(ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class ShopCategoryModelSerializer(ModelSerializer):
    class Meta:
        model = ShopCategory
        fields = '__all__'


class LanguageModelSerializer(ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class CountryModelSerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
