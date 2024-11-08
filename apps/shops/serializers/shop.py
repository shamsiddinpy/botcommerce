from django.shortcuts import get_object_or_404
from rest_framework.fields import CurrentUserDefault, HiddenField, ListField, CharField, SerializerMethodField
from rest_framework.serializers import ModelSerializer

from shops.models import (Attachment, Country, Currency, Language,
                          Shop, ShopCategory)
from users.models import Plan, Quotas, PlanPricing


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


class LanguagesModelSerializer(ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class PlanPricingModelSerializer(ModelSerializer):
    class Meta:
        model = PlanPricing
        fields = '__all__'


class ShopModelSerializer(ModelSerializer):
    owner = HiddenField(default=CurrentUserDefault())
    languages = ListField(child=CharField(), write_only=True)
    pricing = SerializerMethodField()
    quotas = ListField(child=CharField(), write_only=True)

    class Meta:
        model = Shop
        fields = (
            'id', 'name', 'phone_number', 'shop_category', 'country', 'languages', 'currency', 'owner', 'country',
            "created_at", 'status', 'about_us', 'plan', 'pricing', 'quotas')
        read_only_fields = 'about_us', 'status', 'plan', 'pricing', 'quotas'

    def to_representation(self, instance: Shop):
        data = super().to_representation(instance)
        data['country'] = CountryModelSerializer(instance.country).data
        data['shop_category'] = instance.shop_category.name
        data['shop_currency_id'] = instance.currency.id
        data['languages'] = [lang.code for lang in instance.languages.all()]
        data['has_terminal'] = instance.has_terminal
        data['plan'] = PlanModelSerializer(instance.plan).data
        data['pricing'] = self.get_pricing(instance)
        return data

    def get_pricing(self, instance: Shop):
        pricing_qs = PlanPricing.objects.filter(plan=instance.plan)
        return PlanPricingModelSerializer(pricing_qs, many=True).data

    def create(self, data):
        languages = data.pop('languages', [])
        plan = data.pop('plan', None)
        if not plan:
            plan = get_object_or_404(Plan, code='Free')
        else:
            plan = get_object_or_404(Plan, code=plan)
        language_instances = Language.objects.filter(code__in=languages)  # Todo qaytib kelamn
        shop = Shop.objects.create(**data, plan=plan)
        shop.languages.set(language_instances)
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


class AttachmentModelSerializer(ModelSerializer):
    class Meta:
        model = Attachment
        fields = 'id', 'record_id', 'key', 'url'  # Todo Attachment Rasim yuklaydigan qilish
