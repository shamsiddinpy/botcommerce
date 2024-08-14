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
                              ShopCategoryModelSerializer, ShopModelSerializer)


class ShopModelViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopModelSerializer
    pagination_class = PageSortNumberPagination

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        shop = self.get_object()
        serializer = self.get_serializer(shop, data=self.request.data, partial=True, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        queryset = Category.objects.filter(shop_id=shop_id)
        name = self.request.query_params.get('search', None)
        if name:
            queryset = queryset.filter(name__contains=name)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@extend_schema(tags=['Category'])
class CategoryUpdateAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        data = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [serializer.data],
            "sort_fields": []
        }
        return Response(data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
