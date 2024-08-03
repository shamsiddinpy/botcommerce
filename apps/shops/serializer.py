from rest_framework.fields import CurrentUserDefault, HiddenField, SerializerMethodField
from rest_framework.serializers import ModelSerializer

from shops.models import Country, Currency, Language, Shop, ShopCategory, Category


class DynamicFieldsModelSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class ShopCategoryModelSerializer(ModelSerializer):
    class Meta:
        model = ShopCategory
        fields = '__all__'


class ShopModelSerializer(ModelSerializer):
    owner = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Shop
        fields = (
            'id', 'name', 'phone_number', 'shop_category', 'country', 'languages', 'currency', 'owner', 'country',
            "created_at", 'status', 'about_us')
        read_only_fields = 'about_us', 'status'

    def to_representation(self, instance: Shop):
        data = super().to_representation(instance)
        data['country'] = CountryModelSerializer(instance.country).data
        data['shop_category'] = instance.shop_category.name
        data['shop_currency_id'] = instance.currency.id
        data['has_terminal'] = instance.has_terminal
        return data


class CurrencyModelSerializer(ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class LanguageModelSerializer(ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class CountryModelSerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class CategoryModelSerializer(DynamicFieldsModelSerializer):
    parent = SerializerMethodField()
    owner = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Category
        fields = ('name', 'emoji', 'parent', 'show_in_ecommerce', 'status', 'description', 'position',
                  'shop', 'attachments', 'owner')
        read_only_fields = 'show_in_ecommerce', 'status', 'shop'

    def get_parent(self, instance):
        if instance.parent:
            return {
                'id': instance.parent.id,
                'name': instance.parent.name,
            }
        return {id: None, 'name': ''}

    def to_representation(self, instance: Category):
        cate = super().to_representation(instance)
        cate['show_in_ecommerce'] = instance.show_in_ecommerce
        cate['parent'] = self.get_parent(instance)
        return cate
