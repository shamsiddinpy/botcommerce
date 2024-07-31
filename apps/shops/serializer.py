from rest_framework.fields import CurrentUserDefault, HiddenField
from rest_framework.serializers import ModelSerializer
from shops.models import Country, Currency, Language, Shop, ShopCategory, Category


class ShopModelSerializer(ModelSerializer):
    owner = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Shop
        fields = (
            'id', 'name', 'phone_number', 'shop_category', 'country', 'languages', 'currency', 'owner', 'country_id',
            "created_at", "shop_category_id", 'status')

    def to_representation(self, instance: Shop):
        data = super().to_representation(instance)
        data['country'] = CountryModelSerializer(instance.country).data
        data['shop_category'] = instance.shop_category.name
        data['shop_currency_id'] = instance.currency.id
        data['status'] = instance.status
        return data


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


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ''
