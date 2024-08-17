from csv import DictReader
from io import TextIOWrapper

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import (ListAPIView,
                                     ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from shared.django.pagination import PageSortNumberPagination
from shops.models import (Category, Country, Currency, Language, Shop,
                          ShopCategory)
from shops.serializer import (CategoryModelSerializer, CountryModelSerializer,
                              CurrencyModelSerializer, LanguageModelSerializer,
                              ShopCategoryModelSerializer, ShopModelSerializer, FileUploadSerializer)


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


@extend_schema(tags=['Category'])
class CategoryCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    pagination_class = PageSortNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

    def get_queryset(self):
        shop_id = self.kwargs['shop_id']
        return Category.objects.filter(shop_id=shop_id)


@extend_schema(tags=['Category'])
class CategoryUpdateAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()
    pagination_class = PageSortNumberPagination


@extend_schema(tags=['CategoryImport'])
class CategoryImportAPIView(ListCreateAPIView):
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file was uploaded."}, status=status.HTTP_400_BAD_REQUEST)
        rows = TextIOWrapper(file)
        for row in DictReader(rows):
            print(row)
        return Response({"status": "File uploaded and processed successfully."})
