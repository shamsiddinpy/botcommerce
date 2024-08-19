from drf_spectacular.utils import extend_schema
from rest_framework.generics import (ListAPIView)
from rest_framework.viewsets import ModelViewSet

from shared.django.pagination import PageSortNumberPagination
from shops.models import (Country, Currency, Language, Shop,
                          ShopCategory)
from shops.serializers.serializers_shop import (CountryModelSerializer,
                                                CurrencyModelSerializer, LanguageModelSerializer,
                                                ShopCategoryModelSerializer, ShopModelSerializer)


@extend_schema(tags=['shops'])
class ShopModelViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopModelSerializer
    pagination_class = PageSortNumberPagination

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


@extend_schema(tags=['Api'])
class ShopCategoryListAPIView(ListAPIView):
    queryset = ShopCategory.objects.all()
    serializer_class = ShopCategoryModelSerializer


@extend_schema(tags=['Api'])
class CurrencyListAPIView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencyModelSerializer
    pagination_class = None


@extend_schema(tags=['Api'])
class LanguageListAPIView(ListAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageModelSerializer
    pagination_class = None


@extend_schema(tags=['Api'])
class CountryListAPIView(ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryModelSerializer
