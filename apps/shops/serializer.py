from django.shortcuts import get_object_or_404
from jsonschema import ValidationError
from rest_framework.fields import CurrentUserDefault, HiddenField, SerializerMethodField
from rest_framework.serializers import ModelSerializer

from shops.models import Country, Currency, Language, Shop, ShopCategory, Category, Attachment
from users.models import Plan, Quotas


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


class QuotasModelSerializer(ModelSerializer):
    class Meta:
        model = Quotas
        fields = '__all__'


class PlanModelSerializer(ModelSerializer):
    quotas = QuotasModelSerializer(read_only=True, many=True)

    class Meta:
        model = Plan
        fields = 'name', 'description', 'code', 'quotas'
        read_only_fields = ['quotas']


class ShopModelSerializer(ModelSerializer):
    owner = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Shop
        fields = (
            'id', 'name', 'phone_number', 'shop_category', 'country', 'languages', 'currency', 'owner', 'country',
            "created_at", 'status', 'about_us', 'plan')
        read_only_fields = 'about_us', 'status', 'plan',

    def to_representation(self, instance: Shop):
        data = super().to_representation(instance)
        data['country'] = CountryModelSerializer(instance.country).data
        data['shop_category'] = instance.shop_category.name
        data['shop_currency_id'] = instance.currency.id
        data['has_terminal'] = instance.has_terminal
        data['plan'] = PlanModelSerializer(instance.plan).data
        return data

    def create(self, data):
        languages = data.pop('languages', [])
        plan = data.pop('plan', None)
        if not plan:
            plan = get_object_or_404(Plan, code='Free')
        shop = Shop.objects.create(**data, plan=plan)
        shop.languages.set(languages)
        return shop


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


class AttachmentDynamicFieldsModelSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Attachment
        fields = 'content_type', 'record_id', 'key', 'url'


class CategoryModelSerializer(DynamicFieldsModelSerializer):
    owner = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Category
        fields = ('name', 'emoji', 'parent', 'show_in_ecommerce', 'status', 'description', 'position',
                  'shop', 'attachments', 'owner')
        read_only_fields = 'show_in_ecommerce', 'status', 'shop'

    def to_representation(self, instance: Category):
        cate = super().to_representation(instance)
        cate['show_in_ecommerce'] = instance.show_in_ecommerce
        cate['parent'] = instance.parent
        return cate

    def validate(self, data):
        shop_id = self.context.get('shop_id')
        if data.get('parent'):
            if data['parent'].shop_id != shop_id:
                raise ValidationError({"parent": "Kategoriya boshqa do'konga tegishli"})
        return data
