from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from shops.models import Currency, Language, Shop, Country, ShopCategory
from shops.serializer import CurrencyModelSerializer, LanguageModelSerializer, ShopModelSerializer, \
    CountryModelSerializer, ShopCategoryModelSerializer


# Create your views here.
class ShopCreateAPIView(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopModelSerializer
    permission_classes = IsAuthenticated,
    pagination_class = None

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = ShopModelSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ShopCategoryListAPIView(ListAPIView):
    queryset = ShopCategory.objects.all()
    serializer_class = ShopCategoryModelSerializer

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class CurrencyListAPIView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencyModelSerializer
    pagination_class = None


class LanguageListAPIView(ListAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageModelSerializer
    pagination_class = None


class CountryListAPIView(ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryModelSerializer
